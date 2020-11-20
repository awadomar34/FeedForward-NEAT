# About
This project was created for the purpose of learning. Particuarly, to gain insights in to Neuorevolution and to gain an understanding of Deep Learning, in general. If you would like to use NEAT in your own implementation or product, I would recomment [CodeReclaimer's neat-python](https://github.com/CodeReclaimers/neat-python), the offical NEAT library, as it was the inspiration for this project and has fewer scaling isssues and allows for more functionality than this project, such as: evolving RNNs, CTRNNs, built in Node Bias and Response attributes, etc.

## To Test This Project
Download this project and extract the repo.
Open the main directory in a terminal (command prompt for Windows users)
Run the command:
```bash
python __init__.py
```

will run one of the following tests: 
Markup: *XOR test
        *Single Pole Balancing test

you can comment/uncomment a the test you would like to run.

## Tests
From the files in Tests, you can change:
-the number of times these tests are preformed
-whether or not the result of each test is written to a file

##
In NEAT, are the files of which run the NEAT algorithm. The files are the class files of Genome, Species and Population.

In Network, are the files which are used to create phenotypes. The files are the class files which make feed-forward networks.

In Simulations, are the files which have the tests in them. These tests are the XOR problem and the Single Pole Balancing test.

##
conn_history and node_history are used to store the innovation history of the currently running population
