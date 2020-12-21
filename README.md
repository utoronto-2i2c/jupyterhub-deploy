# 2i2c JupyterHub for University of Toronto

Check it out at [jupyter.utoronto.ca](https://jupyter.utoronto.ca)

## Pulling from private GitHub repos with nbgitpuller

GitHub is used to store class materials (lab notebooks, lecture notebooks, etc), and
[nbgitpuller](https://jupyterhub.github.io/nbgitpuller/) is used to distribute it
to students. By default, nbgitpuller only supports public GitHub repositories. However,
University of Toronto JupyterHub is set up to allow pulling from private repositories
as well. 

Public repositories are still preferred, but if you want to distribute a private repository
to your students, you can do so by adding [installing this GitHub app](https://github.com/apps/utoronto-jupyterhub-private-cloner)
in your private repository.a [deploy key](https://docs.github.com/en/free-pro-team@latest/developers/overview/managing-deploy-keys#deploy-keys)
to your private repository.

1. Go to the [University of Toronto JupyterHub Private Repo Access](https://github.com/apps/utoronto-jupyterhub-private-cloner)

2. Click the 'Install' button.

3. Select the organization / user containing the private repository you want to distribute
   on the JupyterHub. If you are not the owner or administrator of this organization, you might
   need extra permissions to do this action.
   
4. Select 'Only select repositories', and below that select the private repositories you want
   to distribute to this JupyterHub.
   
5. Click the 'Install' button.

That's it! You're all set. You can now make nbgitpuller links at [nbgitpuller.link](http://nbgitpuller.link)
as before, and it'll work for everyone authenticated to jupyter.utoronto.ca.

Note: *Everyone* on the University of Toronto JupyterHub can use nbgitpuller to clone
your private repo if you do this. They won't be able to see that this repo exists,
but if they get their hands on your nbgitpuller link they can fetch that too. More
fine-grained permissions coming soon.
