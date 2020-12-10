#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Michael Pechner <mikey@mikey.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


DOCUMENTATION = r'''
---
module: ecs_capacity_provider
version_added: 1.0.0
short_description: create and remove Amazon ECS capcity providers
notes:
    - none
description:
    - Creates and removes tags for Amazon ECS capacity providers.
author:
  - Michael Mayer (@mjmayer)
requirements: [ boto3, botocore ]
options:
  name:
    description:
      - The name of the ECS capcity provider
    required: true
    type: str
  auto_scaling_group_arn:
    description:
      - The ARN of the autoscaling group this capacity provider will be associated with.
    required: true
    type: str
  termination_protection:
    description:
      -  This determines whether the Auto Scaling group has managed termination protection.
    required: false
    type: str
  mangaged_scaling:
    description:
      - The managed scaling settings for the Auto Scaling group capacity provider.
    required: false
    type: dict
      suboptions:
        status:
          type: bool
          description: Whether or not to enable managed scaling for the capacity provider.
        target_capacity:
          type: int
          description: The target capacity value for the capacity provider.
                       The specified value must be greater than 0 and less than or equal to 100.
                       A value of 100 will result in the Amazon EC2 instances in your Auto Scaling
                       group being completely utilized.
        min_scaling_step_size:
          type: int
          description: The minimum number of container instances that Amazon ECS will scale in or scale out at one time.
        max_scaling_step_size:
          type: int
          description: The maximum number of container instances that Amazon ECS will scale in or scale out at one time.
        instance_warmup_period:
          type: int
          description: Period of time in seconds before a newly launch instance can contribute to CloudWatch metrics for
                       the Auto Scaling Group.
  state:
    description:
      - Whether the ECS capcity provider should be present or absent.
    default: present
    choices: ['present', 'absent']
    type: str
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2

'''

EXAMPLES = r'''
- name: Create ECS capacity provider
  community.aws.ecs_capacity_provider:
    auto_scaling_group_arn: arn:aws:autoscaling:us-west-2...
  state: present

- name: Create managed ECS capacity provider
  community.aws.ecs_capacity_provider:
    auto_scaling_group_arn: arn:aws:autoscaling:us-west-2...
    managed_scaling:
      - status: enabled
        target_capacity: 1
        min_scaling_step_size: 1
        max_scaling_step_size: 10000
        instance_warmup_period: 300
  state: present

- name: Delete ECS capacity provider
  community.aws.ecs_capacity_provider:
    auto_scaling_group_arn: arn:aws:autoscaling:us-west-2...
  state: absent
'''

RETURN = r'''
capacityProvder:
    description: Full description of the capacity provider
    returned: when creating a capacity provider
    type: complex
    contains:
        capacityProviderArn:
            description: The Amazon Resource Name (ARN) of the of the capacity provider.
            returned: always
            type: str
        name:
          description: Name of the capacity provider.
          returned: always
          type: str
        status:
          description: Current status of the capacity provider
          returned: always
          type: str
        autoScalingGroupProvider:
          description: The Auto Scaling group settings for the capacity provider.
          returned: always
          type: complex
          contains:
            autoScalingGroupProvider:
              description: The ARN that identifies the Auto Scaling Group
              returned: always
              type: str
            managedScaling:
              description: The managed scaling settings for the Auto Scaling group capacity provider
              returned: always
              type: complex
              contains:
                status:
                  description: Whether or not to enable managaged scaling for the capacity provider.
                  returned: always
                  type: str
                targetCapacity:
                  description: The target capacity value for the capacity provider
                  returned: always
                  type: int
                minimumScalingStepSize:
                  description: The minimum number of container instances that Amazon
                               ECS will scale in or scale out at one time.
                  returned: always
                  type: int
                maximumScalingStepSize:
                  description: The maximum number of container instances that Amazon
                               ECS will scale in or scale out at one time.
                  returned: always
                  type: int
                instanceWarmupPeriod:
                  description: Number of seconds before the instance will start
                               contributing the CloudWatch Metrics.
                  returned: always
                  type: int
            managedTerminationProtection:
              description: The managed termination protection setting.
              returned: always
              type: str
        updateStatus:
          description: The update status of the capacity provider
          returned: always
          type: str
        updateReason:
          description: Provides details about the update status of the capacity provider
          returned: always
          type: str
'''

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule

try:
    import boto3
    import botocore
except ImportError:
    pass    # Handled by AnsibleAWSModule
__metaclass__ = type

class CapacityProviderManager:
    """Handles Capacity Providers"""

    def __init__(self, module):
        self.module = module
        try:
            self.ecs = module.client('ecs')
        except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
            module.fail_json_aws(e, msg='Failed to connect to AWS')

    def create_capacity_provider(self, capacity_provider_name, auto_scaling_group_arn,
                                 termination_protection, managed_scaling)


        params = dict(
            name=capacity_provider_name,


            cluster=cluster_name,
            serviceName=service_name,
            taskDefinition=task_definition,
            loadBalancers=load_balancers,
            clientToken=client_token,
            role=role,
            deploymentConfiguration=deployment_configuration,
            placementConstraints=placement_constraints,
            placementStrategy=placement_strategy
        )
        if network_configuration:
            params['networkConfiguration'] = network_configuration
        if launch_type:
            params['launchType'] = launch_type
        if self.health_check_setable(params) and health_check_grace_period_seconds is not None:
            params['healthCheckGracePeriodSeconds'] = health_check_grace_period_seconds
        if service_registries:
            params['serviceRegistries'] = service_registries
        # desired count is not required if scheduling strategy is daemon
        if desired_count is not None:
            params['desiredCount'] = desired_count
        if scheduling_strategy:
            params['schedulingStrategy'] = scheduling_strategy
        if capacity_provider_strategy:
            params['capacityProviderStrategy'] =  capacity_provider_strategy

        response = self.ecs.create_service(**params)
        return self.jsonize(response['service'])

def main():
    argument_spec = dict(
        state=dict(required=True, choices=['present', 'absent', 'deleting']),
        name=dict(required=True, type=str),
        capacity_providers=(type=list, elements=dict)
    )
    module = AnsibleAWSModule(argument_spec=argument_spec,
                              required_if=[('state', 'present', ['capacity_providers'])])
    state = module.params.get('state')
if __name__ == '__main__':
    main()
