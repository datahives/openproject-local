# Local OpenProject.org Launcher

This is a wrapper application to launch the local running [OpenProject.org](https://openproject.org) easily.
The launcher checks for the Docker daemon's status, pull and run the official OpenProject container image, and configure it to work with a local copy of the data.

The local data can be sync with any cloud syncing solution.

**Warning** 

This local configuration is not suitable for multi-user usage, as syncing the database across multiple users will break the its integrity. Instead install the OpenProject on a webserver following the instruction on OpenProject website.