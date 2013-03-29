#
# Newfies-Dialer License
# http://www.newfies-dialer.org
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2013 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.intermediate_model_base_class import Model
from user_profile.models import Manager
from agent.models import AgentProfile


class Queue(Model):
    """This defines the callcenter queue

    **XML output**:
        <param name="strategy" value="agent-with-least-talk-time"/>
        <param name="moh-sound" value="$${hold_music}"/>
        <param name="record-template" value="$${base_dir}/recordings/sales/${strftime(%Y-%m-%d-%H-%M-%S)}.${destination_number}.${caller_id_number}.${uuid}.wav"/>
        <param name="time-base-score" value="queue"/>
        <param name="tier-rules-apply" value="false"/>
        <param name="tier-rule-wait-second" value="300"/>
        <param name="tier-rule-wait-multiply-level" value="true"/>
        <param name="tier-rule-no-agent-no-wait" value="false"/>
        <param name="discard-abandoned-after" value="14400"/>
        <param name="abandoned-resume-allowed" value="True"/>
        <param name="max-wait-time" value="0"/>
        <param name="max-wait-time-with-no-agent" value="120"/>
        <param name="max-wait-time-with-no-agent-time-reached" value="5"/>

    **Attributes**:

        * ``strategy`` - Queue strategy
        * ```` -


    **Relationships**:

        * ``manager`` - Foreign key relationship to the manager model.

    **Name of DB table**: queue
    """
    manager = models.ForeignKey(Manager,
                                verbose_name=_("manager"), blank=True, null=True,
                                help_text=_("select manager"), related_name="queue manager")
    strategy = models.CharField(verbose_name=_("strategy"),
                                max_length=120, null=True, blank=True)
    moh_sound = models.CharField(verbose_name=_("moh-sound"),
                                max_length=250, null=True, blank=True)
    record_template = models.CharField(verbose_name=_("record-template"),
                                max_length=250, null=True, blank=True)
    time_base_score = models.CharField(verbose_name=_("time-base-score"),
                                max_length=50, null=True, blank=True)
    tier_rules_apply = models.BooleanField(default=True, verbose_name=_("tier-rules-apply"))
    tier_rule_wait_second = models.IntegerField(verbose_name=_("tier-rule-wait-second"),
                                max_length=250, null=True, blank=True)
    tier_rule_wait_multiply_level = models.BooleanField(default=True,
                                            verbose_name=_("tier-rule-wait-multiply-level"))
    tier_rule_no_agent_no_wait = models.BooleanField(default=True,
                                                     verbose_name=_("tier-rule-no-agent-no-wait"))
    discard_abandoned_after = models.IntegerField(verbose_name=_("discard-abandoned-after"),
                                                  max_length=250, null=True, blank=True)
    abandoned_resume_allowed = models.BooleanField(default=True,
                                                   verbose_name=_("abandoned-resume-allowed"))
    max_wait_time = models.IntegerField(verbose_name=_("max-wait-time"),
                                        max_length=250, null=True, blank=True)
    max_wait_time_with_no_agent = models.IntegerField(verbose_name=_("max-wait-time-with-no-agent"),
                                                      max_length=250, null=True, blank=True)
    max_wait_time_with_no_agent_time_reached = models.IntegerField(verbose_name=_("max-wait-time-with-no-agent-time-reached"),
                                                                   max_length=250, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('date'))
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = u'callcenter_queue'
        verbose_name = _("queue")
        verbose_name_plural = _("queues")

    def __unicode__(self):
            return u"%s [%s]" % (self.id, self.request_uuid)


class Tier(Model):
    """This defines the callcenter tier

    **XML output**:
        <!-- If no level or position is provided, they will default to 1.  You should do this to keep db value on restart. -->
        <!-- agent 1000 will be in both the sales and support queues -->
        <tier agent="1000@default" queue="sales@default" level="1" position="1"/>
        <tier agent="1000@default" queue="support@default" level="1" position="1"/>
        <!-- agent 1001 will only be in the support queue -->
        <tier agent="1001@default" queue="support@default" level="1" position="1"/>

    **Attributes**:

        * ``request_uuid`` - Unique id
        * ```` -


    **Relationships**:

        * ``manager`` - Foreign key relationship to the manager model.

    **Name of DB table**: queue
    """
    manager = models.ForeignKey(Manager,
                                verbose_name=_("manager"), blank=True, null=True,
                                help_text=_("select manager"), related_name="tier manager")
    agent = models.ForeignKey(AgentProfile,
                              verbose_name=_("agent"), blank=True, null=True,
                              help_text=_("select agent"), related_name="agent")
    queue = models.ForeignKey(Queue,
                              verbose_name=_("queue"), blank=True, null=True,
                              help_text=_("select queue"), related_name="queue")
    level = models.IntegerField(verbose_name=_("level"), default=1)
    position = models.IntegerField(verbose_name=_("position"), default=1)

    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('date'))
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = u'callcenter_tier'
        verbose_name = _("tier")
        verbose_name_plural = _("tiers")

    def __unicode__(self):
            return u"%s [%s]" % (self.id, self.request_uuid)