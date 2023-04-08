#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Sebastian Widmann
# Institution : TU Munich, Department of Aerospace and Geodesy
# Created Date: March 29, 2023
# version ='1.0'
# ---------------------------------------------------------------------------

import flax.linen as nn


class MultiLayerPerceptron(nn.Module):
    """
    Multilayer perceptron layer

    Attributes
    ----------
    dim_model: int
        dimensionality of embeddings
    dim_mlp: int
        dimensionality of multilayer perceptron layer
    dropout_rate: float
        Dropout rate. Float between 0 and 1.
    """

    dim_model: int
    dim_mlp: int
    dropout_rate: float = 0.1

    @nn.compact
    def __call__(self, input_mlp, deterministic):
        """
        Applies MLP layer on the inputs.

        Parameters
        ----------
        input_mlp: TODO: add dtype
            TODO: Add description
        deterministic: bool
            If false, the attention weight is masked randomly using dropout,
            whereas if true, the attention weights are deterministic.

        Returns
        -------
        TODO: add dtype
            Output of MLP layer.
        """

        x = nn.Dense(features=self.d_mlp)(input_mlp)
        x = nn.gelu(x)
        x = nn.Dropout(rate=self.dropout_rate, deterministic=deterministic)(x)
        x = nn.Dense(features=self.d_model)(x)
        x = nn.Dropout(rate=self.dropout_rate, deterministic=deterministic)(x)
        return x
