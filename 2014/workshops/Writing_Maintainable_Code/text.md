#Writing Maintainable Code - Peter Inglesby

A few thoughts on maintainability and complexity

"Always write code as if the person who ends up maintaining it is a violent psychopath who knows where you live..." [0]

Maintainable code is easy to read, easy to understand, and easy to extend. Very little of the code we write is never maintained, so making it maintainable must be one of our goals.  I don't think anybody would disagree with this.

However, we've all experienced code that is a nightmare to maintain.  Week-long sprints to extend a little bit of functionality have become months-long marathons once the true extent of maintainability problems becomes clear.

Moreover, we've all been responsible for producing unmaintainable code.  (If you haven't, you can stop reading now!)

So, despite our best efforts, we fail at writing maintainable code.  Why is it so hard?

Code becomes unmaintainable when it is too complex to understand.  You might argue that having complexity in our code is natural because, as programmers, we're solving complex problems.  Ironically, I think this view is too simple.

In his 1987 essay "No Silver Bullet" [1], Fred Brooks demonstrates that there are two kinds of complexity.  He contrasts "essential" [2] complexity with "accidental" [3] complexity.

Essential complexity is inherent to a problem.  It's unavoidable, and it must be understood before we can attempt to properly solve it.

On the other hand, accidental complexity is what we bring to the problem when we try to solve it.  Accidental complexity comes in two kinds.

The first relates to our tools.  Do our tools help us solve problems, or do they get in the way?  I think this is something we're getting better at.  For instance, with a high level language such as Python, we don't have to think about things like manual memory management.

The second kind of accidental complexity is what we, as programmers, create through our code.  This is something that we still struggle with.

For instance, we often create accidental complexity when we spend too much time writing code to solve problems that we might face in the future, leading to unnecessary abstractions that are hard to understand.

Conversely, we create accidental complexity when we write new code quickly and don't give enough thought to how this new code relates to the rest of a codebase.  This can lead to repetitious and poorly structured code that is, again, hard to understand.

In order for our code to be maintainable, it must expose the essential complexity of the problem that we're trying to solve, while avoiding adding too much accidental complexity.  For this to happen, the structure of the code must correspond with the essential structure of the underlying problem.

My workshop, "Writing Maintainable Code", will be about identifying the essential structures of the problems we're trying to solve, and about writing code so that these essential structures are clear and visible.

During the workshop, we'll practice refactoring code to become better structured.  Although the examples will all be on a small scale, the ideas and the techniques we'll explore will be applicable at a larger scale.

My hope is that workshop will help you write code that is easier to read, to understand, and to extend, and that this will help protect you from that violent psychopath who knows where you live!

[0] http://stackoverflow.com/questions/876089  
[1] http://www.cs.nott.ac.uk/~cah/G51ISS/Documents/NoSilverBullet.html  
[2] "Essence", from a Latin word meaning "to be"  
[3] "Accidence", from a Latin word meaning "to happen alongside"  

<!-- Przeczytane: Piotr Kasprzyk -->
