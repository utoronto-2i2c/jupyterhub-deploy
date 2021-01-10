import asyncio
import argparse
import uuid
import time
from contextlib import asynccontextmanager

from jupyterhub_client.api import JupyterHubAPI, JupyterAPI
from jupyterhub_client.utils import parse_notebook_cells, tangle_cells


@asynccontextmanager
async def use_user_server(hub, username):
    """
    Start a server for username on hub, cleaning up when done
    """
    try:
        await hub.ensure_user(username, create_user=True)
        print(f'{username}: created user')
        try:
            await hub.ensure_server(username, create_user=False)
            print(f'{username}: created server')
            yield
        finally:
            # Even if hub.create_server(username) doesn't finish, hub may still create the
            # user's server if the request got to it. Let's make sure there's no server running for the user.
            # Otherwise, users' single-servers will continue to run and hub will return
            # "SingleUserNotebookApp mixins:520] Error notifying Hub of activity"
            await hub.delete_server(username)
            while True:
                user = await hub.get_user(username)
                if not user['servers']:
                    break
                await asyncio.sleep(1)
            print(f'{username}: deleted server')
    finally:
        await hub.delete_user(username)
        print(f'{username}: deleted user')

@asynccontextmanager
async def use_kernel(hub, username):
    """
    Start a kernel for username on hub, cleaning up when done.

    Assumes the server has already been started.
    """
    user_server = JupyterAPI(hub.hub_url / 'user' / username, hub.api_token)
    async with user_server:
        kernel_id, kernel = await user_server.ensure_kernel(kernel_spec=None)
        print(f'{username}: started kernel')
        try:
            async with kernel:
                yield kernel
        finally:
            await user_server.delete_kernel(kernel_id)
            print(f'{username}: delete kernel')

async def run_user_notebook(hub_url, cells, token=None):
    server_started = False
    notebook_executed = False

    hub = JupyterHubAPI(hub_url=hub_url, api_token=token)

    async with hub:
        token = await hub.identify_token(hub.api_token)
        service_name = token['name']
        username = f'service-{service_name}-{uuid.uuid4()}'

        async with use_user_server(hub, username) as user:
            async with use_kernel(hub, username) as kernel:
                for i, (code, expected_result) in enumerate(cells):
                    kernel_result = await kernel.send_code(username, code, wait=True)
                    if kernel_result != expected_result:
                        print(f'Kernel result did not match expected result')

    return True

async def run_stress_test(hub_url, num_users, notebook_path, timeout, token):
    cells = parse_notebook_cells(notebook_path)

    tasks = [run_user_notebook(hub_url, cells, token) for i in range(num_users)]
    _done, _running = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED, timeout=timeout)
    
    print(f'Done: {len(_done)}')
    print(f'Running: {len(_running)}')
    
    full_success = len(_done) * 100 / num_users
    print(f"Full success = {full_success}%")

    for task in _running:
        task.cancel()
        await task

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
