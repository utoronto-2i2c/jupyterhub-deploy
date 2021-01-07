import asyncio
import argparse
import uuid

from jupyterhub_client.api import JupyterHubAPI
from jupyterhub_client.utils import parse_notebook_cells, tangle_cells

servers_lock = asyncio.Lock()
servers_started = 0
notebooks_lock = asyncio.Lock()
notebooks_executed = 0

async def run_user_notebook(notebook_path):
    global servers_started
    global notebooks_executed

    cells = parse_notebook_cells(notebook_path)
    hub = JupyterHubAPI("http://localhost:8000")

    async with hub:
        token = await hub.identify_token(hub.api_token)
        service_name = token['name']
        username = f'service-{service_name}-{uuid.uuid4()}'
        try:
            jupyter = await hub.ensure_server(username, user_options=None, create_user=True)
            # Count servers started successfully
            async with servers_lock:
                servers_started += 1
            async with jupyter:
                kernel_id, kernel = await jupyter.ensure_kernel(kernel_spec=None)
                async with kernel:
                    for i, (code, expected_result) in enumerate(cells):
                        kernel_result = await kernel.send_code(username, code, wait=True)
                        if kernel_result != expected_result:
                            print(f'kernel result did not match expected result')
                # Count notebook executed successfully
                async with notebooks_lock:
                    notebooks_executed += 1
                await jupyter.delete_kernel(kernel_id)
            await hub.delete_server(username)
        finally:
            await hub.delete_user(username)

async def run_stress_test(num_users, notebook, timeout):
    tasks = [run_user_notebook(notebook) for i in range(num_users)]
    _done, _running = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED, timeout=timeout)
    
    print(f'Done: {len(_done)}')
    print(f'Running: {len(_running)}')
    
    full_success = len(_done) * 100 / num_users
    print(f"Full success = {full_success}%")

    server_success = (servers_started - notebooks_executed) * 100 / num_users
    print(f"Server success = {server_success}%")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-users",
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
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_stress_test(args.num_users, args.notebook, args.test_time_period))
    
if __name__ == "__main__":
    main()
