# Lets create a Pluggable system using abstraction, interface and subclasses

# Pluggable system is system where one entity plugs into another to extend functionality
# But the system will still do ok without plugging another plugins

# Lets implement

class Animal:
    def speak(self):
        raise NotImplementedError


class Cat(Animal):
    def speak(self):
        print("Meow.")


class Dog(Animal):
    def speak(self):
        print("Woof.")


# In this example, Animal is an abstraction: it declares its speak method,
#  but it’s not intended to be run (as is signalled by the NotImplementedError).

# Cat and Dog, however, are implementations: they both implement the speak method, each in their own way.

# The speak method can be thought of as an interface: a common way in which other code may interact with these classes.

# Polymorphism and duck typing

# Because Cat and Dog implement a shared interface, we can interact with either class without knowing which one it is:

def make_animal_speak(animal):
    animal.speak()

    
make_animal_speak(Cat())
make_animal_speak(Dog())

# The make_animal_speak function need not know anything about cats or dogs;
#  all it has to know is how to interact with the abstract concept of an animal. Interacting with objects without knowing their specific type, only their interface, is known as ‘polymorphism’.

# Of course, in Python we don’t actually need the base class:

class Cat:
    def speak(self):
        print("Meow.")


class Dog:
    def speak(self):
        print("Woof.")


# Even if Cat and Dog don’t inherit Animal, they can still be passed to make_animal_speak and things will work just fine. 
# This informal ability to interact with an object without it explicitly declaring an interface is known as ‘duck typing’.


