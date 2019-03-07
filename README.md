# IMAGENT watcher
#### Work in Progress

Apparently the system process `imagent` is broken in Mac OS Sierra. 
It consumes more memory than it should making your computer incredibly **SLOW** (up to `4GB` and it keeps going unless you stop it).
In Mac OS Mojave it consumes up to `30MB` which is alright. 

This script will watch and kill the process if it reaches the specified threshold (`60MB` by default)

The easiest solution would be upgrading to the latest OS. However I know that some people can't do this
because some stuff is still not supported in Mojave. So if you are one of us I hope this helps you 👍
