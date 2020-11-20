# About
This project was created for learning and academic purposes. Particularly, to gain deep insights into the field Neuroevolution and to gain an understanding of Deep Learning, in general. If you would like to use a NEAT implementation as part of your own implementation or product, I would recommend [CodeReclaimer's neat-python](https://github.com/CodeReclaimers/neat-python), the offical NEAT library, as it was the inspiration for this project and has fewer scaling isssues and allows for more functionality than this project, such as: evolving RNNs, CTRNNs, built in Node Bias and Response attributes, etc.

## To Test This Repo
Download this project and extract the files.
Open the main directory in a terminal (command prompt for Windows users)
Run the command:
```bash
python3 __init__.py
```
or, for Windows users,
```bash
python __init__.py
```

will run one of the following tests: 
* XOR test
* Single Pole Balancing test

you can comment/uncomment the test you would like to run.

## Tests
From the files in Tests, you can change:
* The number of times these tests are preformed
* Whether the result of each test is written to a file

## Repo Organization
In the folder `NEAT`, are the files which implement the NEAT algorithm. 
The files are for the classes Genome, Species and Population. These are the 3 main levels of abstractions required for NEAT.

In the folder `Network`, are the files which are used to create network phenotypes. 
The files are the class files which make feed-forward networks.

In the folder `Simulations`, are the files which have the test enviroments. 
Particularly, I implemented the XOR Problem, for debugging and basic testing purposes, and the Single Pole Balancing Problem as a more complicated environment, to test the effects of different configuration parameters and their effects on the runtime of a simulation with randomised data.

### Innovation History
I used a file-based storage system to store genetic innovation history. Particularly, the innovation history of a population is stored in the files 
`conn_history` and  `node_history`

It is important NOT to run multiple populations at a time as they will share the same files to store innovation history. This will cause the integrity of the populations' innovation histories to be compromised.
