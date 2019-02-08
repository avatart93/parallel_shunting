# Parallel Shunting Yard

This project uses a client-server structure to serve the Shunting Yard algorithm. They communicate through a socket to 
exchange lines of data, in this case math expressions. The server launches children processes to compute the algorithm 
over the received expressions. It communicates with its children with the help of pipes.

WARNING: This project can't yet handle client or server unexpected closures.

## Getting Started

You can either download a zip copy of the project from [github](https://github.com/avatart93/parallel_shunting/) or
directly clone the repository to obtain this project's code:

```
git clone https://github.com/avatart93/parallel_shunting/
```

If you want to include the scripts into your system, please check the install section.

### Prerequisites

This project was implemented using Python 3.7.2 and its standard packages only, so you wont need to install additional 
modules.

### Installing

First, access the project's directory:

```
cd parallel_shunting
```

And type the next command on your console to install the python packages:

```
python setup.py install
```

This will include the project's packages into your python distribution. It will also add some scripts into your system
that will allow you to test and deploy this project.

## Running the tests

If you installed the project, you can use one of the commands to test the project from your console, just type:

```
psy_test
```

If not, you just have to enter the project's directory:

```
cd parallel_shunting
```

and type in your console:

```
python parallel_shunting/tests.py
```

If all tests are correct you should see something like this:

```
All operations tests finished correctly.
All expressions were computed correctly.
Testing asynchronous work.
1 -> Operations batch computed correctly.
2 -> Operations batch computed correctly.
3 -> Operations batch computed correctly.
4 -> Operations batch computed correctly.
5 -> Operations batch computed correctly.
6 -> Operations batch computed correctly.
7 -> Operations batch computed correctly.
8 -> Operations batch computed correctly.
9 -> Operations batch computed correctly.
10 -> Operations batch computed correctly.
All done.
```

### Break down into end to end tests

The test is check if the following features are working properly:

1. Basic math operations.
2. The shunting yard algorithm.
3. Client/Server communication with random delay times.

## Deployment

Once installed, you can launch the server from your console with:

```
psy_server
```

and the client with:

```
psy_client
```

Both scripts will ask you for some directory paths, read carefully and remember that server's processes work in 
parallel so the results you obtain may be unordered. 

WARNING: This project hasn't been enhanced by tools such as cython or numba, so files with more than 300000 operations
can take a couple of minutes to be processed.

## Built With

* [setuptools](https://pypi.org/project/setuptools/) - Used to create and manage packages.

## Authors

* **Gilberto Muñoz** - *All work* - [avatart93](https://github.com/avatart93/)

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details
