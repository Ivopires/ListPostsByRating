# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
from django.utils import timezone
from math import sqrt
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Post(models.Model):
    pub_date = models.DateTimeField('Date Published', default=timezone.now())
    post_text = models.CharField('Post content', max_length=500)
    up_votes = models.PositiveIntegerField('Up votes', default=0)
    down_votes = models.PositiveIntegerField('Down votes', default=0)
    score = models.FloatField('Post Score', default=0)

    def __str__(self):
        return self.post_text

    def compute_score(self):
        """
        The compute_score function will compute the Wilson-score Interval,
        which calculation depends on the number of up/down votes and the total
        number of votes.
        Where:
         - p_hat - is the fraction of up votes out of total votes
         - total_votes - is the total number of votes
         - z - is the normal distribution, which, in order to have 95%
               of confidence, has to be equal to 1.96
        """

        total_votes = self.up_votes + self.down_votes
        if self.up_votes == 0:
            return 0
        else:
            p_hat = np.float64(self.up_votes) / total_votes
            z = np.float64(1.96)

            lower_bound = (((p_hat + z * z / (2 * total_votes)) - z * sqrt(
                (p_hat * (1 - p_hat) + z * z /
                 (4 * total_votes)) / total_votes)) / (1 + z * z / total_votes))

            return lower_bound
