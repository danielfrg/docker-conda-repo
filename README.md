# Docker conda-channel

Docker container to create (and serve) a custom conda channel.

Based on the documentation on [custom channels](http://conda.pydata.org/docs/custom-channels.html)

## Usage

To create a custom channel, first organize all the packages in subdirectories
for the platforms you wish to serve.

```
channel/
  linux-32/
    package-1.0-0.tar.bz
  linux-64/
    package-1.0-0.tar.bz
  osx-64/
    package-1.0-0.tar.bz
  win-64/
    package-1.0-0.tar.bz
  ...
```

Now start the container sharing the `channel` directory as a volume

```
docker run -v $(pwd)/channel:/channel -p 8080:80 danielfrg/conda-channel
```

You can now go to: `http://{DOCKER_HOST}:8080` and see the channel repo.

## Common errors

1. 403 on packages: this is usually because the container user cannot read the
packages. Make sure all the `*.tar.bz2` files are readable by all users:
`chmod 644 *.tar.bz2`
