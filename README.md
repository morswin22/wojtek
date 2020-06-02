# wojtek
W.O.J.T.E.K - Wielka, Obszerna Jednostka Transpozycji Elementarnych Kolumn

## Requirements
All required PyPI modules are listed in `requirements.txt` with their corresponding versions.

You can install them using
```
pip install -r requirements.txt
```

## Usage
After installation simply run
```
python main.py
```
Firstly, you will need to specify a size of a new matrix by writing it on the canvas. 
Next you can fill the canvas with digits as you wish and when all of the cells are filled in,
the matrix decompositions will appear in the console. You can change the values by rewriting the digits.

## Training
`model.h5` contains pretrained CNN model trained on [MNIST](http://yann.lecun.com/exdb/mnist/) hand written digits dataset 

In order to train a new network, you can use
```
python train.py
```
