# OpenMVS Docker

## Introduction

This repository provides modified files to build a docker image from a recent OpenMVS version and an additional Python script to automate the point cloud / mesh generation steps. 

The original OpenMVS library is at: https://github.com/cdcseacave/openMVS

## Build

To build the docker image, run the following command in Linux:

```
. buildFromScratch.sh --cuda
```

## License

This repository and the original OpenMVS library are both licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the license and copyright notice files in the repository. 
