import numpy as np


class Bayes_Bandit:
    """
    Class for performing classical bayesian bandits where item = creative = ad = game_key = line_item_id = AdGroupId
    """

    def __init__(self, initial_beta_matrix=[], items=[]):
        """
        Initilializing beta_matrix and items it contains
        initial_beta_matrix is of shape [Nitems, 2] and items are all the game keys for this campaign, with [a, b] for each game-key
        """

        self.current_beta_matrix = initial_beta_matrix
        self.items = items

    def _add_item(self, item, beta_a=1, beta_b=1):
        """
        Function appends a new item to the items and beta matrix

        Parameters
        ----------
        item : string
            Item key will be added to current beta matrix 
            New game key is initialized to [a,b] = [1,1] as minimally informative priors


        """

        self.items.append(item)
        self.current_beta_matrix.append([beta_a, beta_b])
        pass

    def update(self, item, success, trials):
        """
        Function updates the current beta matrix with new values added using _add_item function, 

        Parameters
        ----------
        item : string
            Some id/key that needs to be updated
        success : number of engagements/first_dropped
            Number of times users engaged with the creative
        trials : number of impressions
            Total number of times the creative was shown to users


        """

        if item not in self.items:
            self._add_item(item)

        ind_item = self.items.index(item)
        self.current_beta_matrix[ind_item][0] += int(success)
        self.current_beta_matrix[ind_item][1] += int(trials - success)

        pass

    def random_draw(self):
        """
        Function creates a beta distribution using [a,b] values and selects a random value from within the distribution, indepependantly for each item 

        Parameters
        ----------
        Beta_matrix : list
            List containing all [a,b] values is converted to a numpy array before randomly drawing from their beta distributions

        Returns
        -------
        rand_draws :  numpy.array
            Array of len(number of items), that contains random probabilites drawn from each of their beta distributions. 
        """

        beta_matrix_arr = np.array(self.current_beta_matrix)
        # draws random beta from each of the items a,b values
        rand_draws = np.random.beta(
            beta_matrix_arr[:, 0], beta_matrix_arr[:, 1])

        return rand_draws

    def pull_lever(self):
        """
        Function uses the randomly drawn distributions from the previous function(rand_draw) to return index of the game/item with the highest probability of success. 

        Parameters
        ----------
        rand_draws : numpy.array
            Random probabilites drawn from each of the items' beta distributions
        items : list of strings
            All game/ad ids

        Returns
        -------
        best game id : string
            ID of the game/item with the highest probability from the drawn beta distributions
        rand_vals : numpy.array
            Array containing the final probabilites of all items. 
            This is returned here because calling the random_draw function randomly draws from beta distributions again, 
            leading to different best game id and probabilties if the two functions are called separately
        """

        # draw from all beta functions
        rand_vals = self.random_draw()

        # get the highest interst
        best_index = np.argmax(rand_vals)
        return np.array(self.items)[best_index]


"""
# to do.

-- add a reset function

-- return probabilites 

-- all the pulling of only a selected number of items

"""
