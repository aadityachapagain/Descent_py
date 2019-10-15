import numpy as np
import math

def Cosine(vec1: np.ndarray, vec2: np.ndarray):
    return np.dot(vec1, vec2.T)/(np.linalg.norm(vec1) * np.linalg.norm(vec2))

def VectorSize(vec: np.ndarray):
    return np.linalg.norm(vec)

def Euclidean(vec1: np.ndarray, vec2: np.ndarray):
    return np.linalg.norm(vec1-vec2)

def Theta(vec1: np.ndarray, vec2: np.ndarray):
    return np.arccos(Cosine(vec1, vec2)) + np.radians(10)

def Triangle(vec1: np.ndarray, vec2: np.ndarray):
    theta = np.radians(Theta(vec1, vec2))
    return (VectorSize(vec1) * VectorSize(vec2) * np.sin(theta))/2

def Magnitude_Difference(vec1: np.ndarray, vec2: np.ndarray):
    return np.abs(VectorSize(vec1) - VectorSize(vec2))

def Sector(vec1: np.ndarray, vec2: np.ndarray):
    ED = Euclidean(vec1, vec2)
    MD = Magnitude_Difference(vec1, vec2)
    theta = Theta(vec1, vec2)
    return math.pi * ((ED + MD)**2) * theta/360


def TS_SS(vec1: np.ndarray, vec2: np.ndarray):
    return Triangle(vec1, vec2) * Sector(vec1, vec2)