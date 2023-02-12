# IMAGENT watcher
#### Work in Progress

The system process `imagent` appears to be broken at least in macOS Sierra or higher. 
It consumes more memory than it should making your computer incredibly **SLOW**
(up to `4GB` and it keeps going unless you stop it).
In Mac OS Mojave it consumes up to `30MB` which is alright. 

This script will watch and kill the process if it reaches the specified threshold (`100MB` by default)

~~The easiest solution would be upgrading to the latest OS.~~
There are occasions when, in macOS Monterey, `imagent` would accumulate memory footprints as large as 25GB+
(Yes, a.k.a. 25,000MB+, I'm not kidding).
~~However I know that some people can't do this because some stuff is still not supported in Mojave.~~
So if you are one of us I hope this woulf help you. 👍

## Pre-requisite
1. python 3.10+
2. `pip3 install psutil`
