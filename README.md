Wired In
========
Task Manager & Time Tracker

### From 'The Social Network'
>SEAN: This house and this team are great. It’s exactly what it should be.
>(to ANDREW)
>I’m Sean Parker.

>ANDREW pays no attention as MARK comes out of the kitchen--

>MARK: He’s _wired in._

>SEAN: That’s what I’m talkin’ about.

About Wired In
----
This is my joint time tracker and task organiser. Sometime around
October 2011 I got fedup using post it notes, text files, complicated
local wordpress installations, etc. to keep track of what I do, how I do
it, and when I do it. I figured with a lot of work I could make a
program that does it better - this is the result, still in progress. 

It is free to use and develop; fork away. I use it daily. I have loaded two example files that show how the information is stored. I would like to move away from .csv eventually.

Some files - my current tasks, lists, and subfunctions - are not included for privacy reasons (obviously, I don't want everyone knwoing what I actually do all day.). These files are privately stored in a bitbucket and should not appear in here.

I originally hadn't intended to make this public - there are a lot of
small bugs that may need to be fixed. There's also a lot of references
to the film Avatar - this started out being called Mask On, the idea
being that I wanted to put my mask on when I went out into the jungle.
Obviously this, and all other references, are merely for my own personal
amusement, and shouldn't be taken too seriously.

Installation
----

Obviously, this is just a python script with various .csv databases.
I run everything from the Terminal and using vi and mvim. If you're not
cool with this, I don't have a solution for you at the moment. I use [Quicksilver](http://www.blacktree.com/) to access the Terminal quickly.

Download the script, and put it somewhere you're happy with it.

Set up an symbolic link - I use `wyr`(and also `mask`)  as an alias:

    ln -s /Users/xyz/long/absolute/path/to/script.py /usr/bin/wyr

Make it executable:

    chmod a+x /Users/xyz/long/absolute/path/to/wired_in.py

Change the path files in the beginning of wired_in.py to your path.
Change file names accordingly. `wyr write` (for tasks), `wyr buy` (for
shopping lists), and `wyr fence` (for the log) will start you out with
an entry in each file. `wyr help` will give you a more-or-less accurate
list of the commands you can use. 

I highly advise that you use this program along with [GeekTools](http://projects.tynsoe.org/en/geektool/) to stop the constant `wyr today tasks all`.
Having it on the desktop is a great, easy, cluttered ux. 

If you have a job and want to keep track of your hours, let me know and
I'll hit you with my personal work python script.