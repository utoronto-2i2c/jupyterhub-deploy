import asyncio
import argparse
import uuid
import time

from jupyterhub_client.api import JupyterHubAPI, JupyterAPI
from jupyterhub_client.utils import parse_notebook_cells, tangle_cells

async def run_user_notebook(hub_url, cells, token=None):
    server_started = False
    notebook_executed = False

    hub = JupyterHubAPI(hub_url=hub_url, api_token=token)

    try:
        async with hub:
            token = await hub.identify_token(hub.api_token)
            service_name = token['name']
            username = f'service-{service_name}-{uuid.uuid4()}'
            user = await hub.ensure_user(username, create_user=True)
            try:
                if user['server'] is None:
                    await hub.create_server(username)
                    try:
                        while True:
                            user = await hub.get_user(username)
                            if user['server'] and user['pending'] is None:
                                jupyter = JupyterAPI(hub.hub_url / 'user' / username, hub.api_token)
                                break
                            await asyncio.sleep(5)
                        # Mark servers started successfully
                        server_started = True
                        async with jupyter:
                            kernel_id, kernel = await jupyter.ensure_kernel(kernel_spec=None)
                            async with kernel:
                                try:
                                    for i, (code, expected_result) in enumerate(cells):
                                        kernel_result = await kernel.send_code(username, code, wait=True)
                                        if kernel_result != expected_result:
                                            print(f'Kernel result did not match expected result')
                                    # Mark notebook executed successfully
                                    notebook_executed = True
                                finally:
                                    print(f"Cleanup: delete kernel of {username}")
                                    await jupyter.delete_kernel(kernel_id)
                    finally:
                        print(f"Cleanup: delete-server of {username}")
                        await hub.delete_server(username)
            finally:
                print(f"Cleanup: make sure no server is being started for user {username}")
                # Even if hub.create_server(username) doesn't finish, hub may still create the
                # user's server if the request got to it. Let's make sure there's no server running for the user.
                # Otherwise, users' single-servers will continue to run and hub will return
                # "SingleUserNotebookApp mixins:520] Error notifying Hub of activity"
                resp = await hub.session.delete(hub.api_url / 'users' / username / 'server')
                while resp.status != 204:
                    resp = await hub.session.delete(hub.api_url / 'users' / username / 'server')
                    status = resp.status
                    await asyncio.sleep(1)

                print(f"Cleanup: delete user and server {username}")
                await hub.delete_user(username)
    except:
        pass

    return (server_started, notebook_executed)

async def run_stress_test(hub_url, num_users, notebook_path, timeout, token):
    cells = parse_notebook_cells(notebook_path)

    tasks = [run_user_notebook(hub_url, cells, token) for i in range(num_users)]
    _done, _running = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED, timeout=timeout)
    
    print(f'Done: {len(_done)}')
    print(f'Running: {len(_running)}')
    
    full_success = len(_done) * 100 / num_users
    print(f"Full success = {full_success}%")

    servers_successful = 0
    for task in _running:
        task.cancel()
        await task
        server_started, notebook_executed = task.result()
        if server_started and not notebook_executed:
            servers_successful += 1

    server_success = servers_successful * 100 / num_users
    print(f"Server success = {server_success}%")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-users",
        type=int,
        default=5,
        help="Number of active users"
    )
    parser.add_argument(
        "--test-time-period",
        type=int,
        default=30,
        help="Test time period"
    )
    parser.add_argument(
        "--notebook",
        default="simple.ipynb",
        help="Notebook to execute"
    )
    parser.add_argument(
        "--api-token",
        help="Notebook to execute"
    )
    parser.add_argument(
        "--hub-url",
        default="http://localhost:8000",
        help="Notebook to execute"
    )

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_stress_test(args.hub_url, args.num_users, args.notebook, args.test_time_period, args.api_token))
    
if __name__ == "__main__":
    main()
