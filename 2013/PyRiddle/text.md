# PyRiddle

## Tomasz Maćkowiak

By combining the best of puzzles, programming, cleverness, speed and prizes we bring you PyRiddle - the Python riddle challenge. Participants will have to raise to the challenge of solving a number of tricky puzzles and compete with each other to win a big prize. A series of tasks will wait for any challenger with his own laptop and a working Internet connection. Be prepared, be focused, as only the first person to solve all the riddles will win the main prize.


### Prizes
The main prize is a brand-new Kindle Paperwhite e-reader, 6" High Resolution Display with Built-in Light and Wi-Fi. Secondary prizes are programming- and puzzle-related books. All prizes are sponsored by STX Next.


### Requirements
Each participant must bring her or his own laptop.

The tasks will be accessible on-line. A working Internet connection and browser are required. The webpage will be publicly visible, so you can use your own Internet access method too (for example using 3G).

Even though the name of the competition is PyRiddle, any way of solving tasks is acceptable. You can solve them in any programming language and with the use of any kind of libraries.
It's highly recommended to have a Python interpreter in your preferred version installed though.

The tasks will be in English, therefore a basic knowledge of the language is required.


### Organization
All participants are required to join the very beginning of the competition event. At the beginning the presenter will reveal the URL address of the riddles’ application. Participants are free to solve the riddles at their own pace, either in the event room or in any location they prefer as long as they have a working Internet connection.

There is no set time limit - whoever finishes all the riddles first wins the main prize. We strongly encourage participants to complete the challenge even if they already know that other contestants have finished before them as there are secondary prizes to be won.
The web application will identify participants using their e-mail addresses. You will be prompted to provide your name and e-mail address.

Solutions don't have to be complete programs. Anything that yields you an expected result is good, for example interactive interpreter sessions or even the use of some external web applications.
Please remember that you will be asked to provide your solutions, whatever form they might have, to ensure that participants do not just input random characters into the forms. Please store your solutions.

The web application will have a limit of requests per user to protect it from brute-force attacks.

Unveiling the winners of the competition, prizes handout, task and discussion about solutions will take place during a separate event.


### Tasks
The precise nature of the tasks is classified. The tasks will require not only programming skills, but also quick thinking, the aptitude for making associations, knowledge of basic algorithms and how the Web works. All riddles will be solvable in a finite amount of time.


### Preparations
Have your favourite development environment ready. At least an editor and a recent Python interpreter is recommended. Python3 is not required, but anything prior to Python2.6 might be missing some useful libraries.

A good idea might be to install Python documentation and then bookmark it in your browser.

	sudo apt-get install python-doc

The competition will involve rapid prototyping so pen and paper might come in handy. A technical aid of a more elaborated interpreter (e.g. ipython) might be useful.

You will most likely have to write small Python programs that you will be running multiple times and enhancing them until they yield expected results. Have a template for those ready:


	import io

	def main():
		with io.open('input.txt', mode='r', encoding='utf-8') as f:
			content = f.read()
		# do something with content
		import pdb; pdb.set_trace()

	if __name__ == '__main__':
		main()

Learn how to inspect live programs using tools like pdb.

Since you will be using a web browser to access the tasks application, have a browser with developer tools ready. Chrome has built-in developer tools, Firefox can have the Firebug extension installed. Learn how to operate such tools.
Keep your mind open, mind the time, remember that it is only the result that counts; therefore your programs can be ugly and buggy as long as they yield the correct result.

***


* [http://pyriddle13.pycon.it](http://pyriddle13.pycon.it) - This year's EuroPython PyRiddle challenge.
* [http://www.pythonchallenge.com/](http://www.pythonchallenge.com/) - The original Python Challenge.
* [http://docs.python.org/2/library/](http://docs.python.org/2/library/) - The Python Standard Library.
* [http://amzn.com/B007OZNZG0](http://amzn.com/B007OZNZG0) - Kindle Paperwhite.
