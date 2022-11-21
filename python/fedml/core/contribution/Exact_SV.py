import logging
import numpy as np
from typing import List, Dict, Callable, Any
from scipy.special import comb


from .base_contribution_assessor import BaseContributionAssessor
from .base_contribution_assessor import powersettool
from .base_contribution_assessor import V_S_t


class Exact_SV(BaseContributionAssessor):
    def __init__(self):
        super().__init__()
        self.SV={} #dict: {id:SV,...}



    def run(
        self,
        num_client_for_this_round: int,
        idxs: List,
        fraction: Dict,  # this is the weights of the clients in FedAvg
        local_weights_from_clients: List[Dict],
        model_aggregated: Dict,
        model_last_round: Dict,
        acc_on_aggregated_model: float,
        val_dataloader: Any,
        validation_func: Callable[[Dict, Any, Any], float],
        device,
    ) -> List[float]:


        N = num_client_for_this_round

        powerset = list(powersettool(idxs))

        util={}

        for S in powerset:
            util[S] = V_S_D(S=S)  # To DO: this is basically training from scratch with the users in set S and return the final test accuracy

        self.SV = self.shapley_value(util, idxs)

        return self.SV

    def shapley_value(self,utility,idxs):
        N=len(idxs)
        sv_dict={id:0 for id in idxs}
        for S in utility.keys():
            if S !=():
                for id in S:
                    marginal_contribution=utility[S]-utility[tuple(i for i in S if i!=id)]
                    sv_dict[id] += marginal_contribution /((comb(N-1,len(S)-1))*N)
        return sv_dict