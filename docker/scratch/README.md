# Hello World!

This is a demonstration of building a binary, creating a Docker image from
scratch, and running with expected output.

## Build the Go Binary

We begin with creating a Go binary compiled for AMD64. Since we are running on
macOS, you need to configure the environment appropriately:

```
export CGO_ENABLED=0
export GOOS=linux
export GOARCH=amd64
```

Then, build the binary from source: `go build hw.go`. Test the binary works as
expected.

```
$ ./hw
-bash: ./hw: cannot execute binary file
```

## Build the Docker image

```
$ docker build -t hw .
Sending build context to Docker daemon  1.775MB
Step 1/3 : FROM scratch
 --->
Step 2/3 : COPY hw /
 ---> 6c0eab7a06fe
Step 3/3 : ENTRYPOINT [ "/hw" ]
 ---> Running in 14a4031906c7
Removing intermediate container 14a4031906c7
 ---> 1cb901113435
Successfully built 1cb901113435
Successfully tagged hw:latest
```