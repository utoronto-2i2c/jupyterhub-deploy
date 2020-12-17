# 2i2c JupyterHub for University of Toronto

Check it out at [jupyter.utoronto.ca](https://jupyter.utoronto.ca)

## Pulling from private GitHub repos with nbgitpuller

GitHub is used to store class materials (lab notebooks, lecture notebooks, etc), and
[nbgitpuller](https://jupyterhub.github.io/nbgitpuller/) is used to distribute it
to students. By default, nbgitpuller only supports public GitHub repositories. However,
University of Toronto JupyterHub is set up to allow pulling from private repositories
as well. 

Public repositories are still preferred, but if you want to distribute a private repository
to your students, you can do so by adding a [deploy key](https://docs.github.com/en/free-pro-team@latest/developers/overview/managing-deploy-keys#deploy-keys)
to your private repository.

1. Go to your repository on GitHub.

2. Go to "Settings", and select "Deploy keys" from the sidebar.

3. Click "Add deploy key" button on the top right

4. Name the key 'University of Toronto JupyterHub', to make it clear what it is for.

5. Copy paste the public key from [this file](https://github.com/utoronto-2i2c/jupyterhub-deploy/blob/staging/deployments/utoronto/config/github-deploy-key.pub)
   to the 'Key'.
   
6. Do *not* check the 'Allow write access' checkbox. If you do, any users on the JupyterHub
   can *push* to your private repository too.
   
7. Click 'Add key' to complete this process.

Once done, you can make nbgitpuller links at [http://nbgitpuller.link] as before, but with
the ssh version of the repository URL. For example, instead of using something like
`https://github.com/utoronto-2i2c/jupyterhub-deploy` for the repo, you should use
`git@github.com:utoronto-2i2c/jupyterhub-deploy.git`. You can also get the ssh URL by
clicking the green 'clone' button in your GitHub repository's page.
