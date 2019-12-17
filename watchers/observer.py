#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod

class Observer(object):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def update(self, obj, arg):
		pass

class Observable(object):

        def __init__(self):    
                self.observers = []

        def add_observer(self, observer):
                if not observer in self.observers:
                        self.observers.append(observer)

        def remove_observe(self, observer):
                if observer in self.observers:
                        self.observers.remove(observer)

        def remove_all_observers(self):
                self.observers = []

        def update(self, arg):
                for observer in self.observers:
                        observer.update(self, arg)