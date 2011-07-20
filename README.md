HandReco
========
HandReco is a handwriting recognition system which uses Hidden Markov Models. It currently supports classification of handwritten words where the letters are separated. It makes use of two levels of HMMs to do the classification. It is first using HMMs to classify the character images and then HMMs to classify words given the output of the previous step. The character images need to fulfill quite hard constraints for it to work good. We believe that we need to optimize the parameters and get more training data for it to be very accurate.

Usage
-----
These instructions help you set up the system so you can test it's basic handwriting recognition capabilities:

1.  Install git (http://help.github.com/mac-set-up-git/)
2.  Clone the project (run the command "git clone git://github.com/kjellwinblad/HandReco.git" in your system terminal)
3.  Install jython 2.5.2 ([www.jython.org](http://www.jython.org/))
4.  Make sure jython is in your "PATH" variable so you can run jython in your system terminal
5.  Open your system terminal and change current directory to where you cloned HandReco (cd path/to/HandReco)
6.  Run the HandReco Writer by running "jython src/__run__.py" in the terminal
7.  Write characters and let the system recognise them!


Project Members
---------------
*   Chongyang Sun ([dorissun](http://github.com/dorissun))
*   Fabian Alenius ([faal](http://github.com/faal))
*   Kjell Winblad ([kjellwinblad](http://github.com/kjellwinblad))
