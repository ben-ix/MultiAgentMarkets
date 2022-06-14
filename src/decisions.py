import numpy as np


def bounded_decision(prior, B, utilities):
    """
    Returns 1/Z * [prior * exp(B * utilities)], where Z is the
    normalizing sum.
    
    This is the soft-max function. Our bounded choice function,
    with some numerical stability tweaks.
    
    """
    # Ensure both are ndarrays
    prior = np.asarray(prior)
    utilities = np.asarray(utilities)

    # Our softmax choice function. 
    weighted_utilities = B * utilities
    weighted_utilities -= weighted_utilities.max()  # Softmax stability
    posterior = prior * np.exp(weighted_utilities)

    # Partition function
    Z = np.sum(posterior)    

    # If Z is 0, it means all values == max(values), so should treat as uniform
    if Z == 0:
        return np.asarray([1 / len(prior)] * len(prior))

    # Normalizes
    posterior /= Z
    
    # Also ensure never becomes exactly zero, else if its used
    # as a prior can never come back into play
    posterior += 1e-08

    return posterior
