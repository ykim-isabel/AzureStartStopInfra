import datetime
import logging
import requests
import os

import azure.functions as func
from ..shared import utils


def main(pausetimer: func.TimerRequest) -> None:
  utc_timestamp = datetime.datetime.utcnow().replace(
    tzinfo=datetime.timezone.utc).isoformat()

  if pausetimer.past_due:
    logging.info('The timer is past due!')

  # getting variables
  logging.info('Getting the variables...')
  ResourceGroupName = os.environ["ResourceGroupName"]
  TenantId = os.environ["TenantId"]
  SubscriptionId = os.environ["SubscriptionId"]
  ServerName = os.environ["DatabaseServerName"]
  DatabaseName = os.environ["DatabaseName"]

  # get the credential
  logging.info('Getting the credential...')
  AppId = os.environ["SynapseAppId"]
  SecretId = os.environ["SynapseSecretId"]

  logging.info('Getting a token...')
  azToken = utils.get_az_token(TenantId, AppId, SecretId)

  pause_synapse(SubscriptionId, azToken, ResourceGroupName, ServerName, DatabaseName)
  logging.info('Synapse Pool paused at %s', utc_timestamp)

def pause_synapse(subscription, token, resourceGroup, server, database):
  url = "https://management.azure.com/subscriptions/"+subscription+"/resourceGroups/"+resourceGroup+"/providers/Microsoft.Sql/servers/"+server+"/databases/"+database+"/pause?api-version=2017-10-01-preview"
  headers = {"Authorization": "Bearer "+token, "Content-Type": "application/json"}
  logging.info('Pausing Synapse pool %s from server %s in resource group %s', database, server, resourceGroup)
  requests.post(url, headers = headers, data='')
