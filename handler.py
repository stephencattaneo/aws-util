'''
    A series of utility lambdas to handle doing automated work.
'''

import logging

import boto3


def shutdown_rds(_event, _context):
    '''
        Handler wrapper for RDSManager.shutdown_rds
    '''

    return RDSManager().shutdown_rds()

def start_rds(_event, _context):
    '''
        Handler wrapper for RDSManager.start_rds
    '''

    return RDSManager().start_rds()

def start_stop_rds(event, _context):
    '''
        Handler wrapper for both RDSManager.shutdown_rds and RDSManager.start_rds.
        Calls one of the two methods, depending on the action in the event.
    '''

    if event['action'] == 'start':
        return RDSManager().start_rds()

    if event['action'] == 'stop':
        return RDSManager().shutdown_rds()

    raise Exception('Unkown action')


class RDSManager:
    '''
        Class for handling RDS related activities.
    '''
    def __init__(self, **kwargs):
        self.log = logging.getLogger(__name__)
        self.log.level = kwargs.get('log_level', logging.DEBUG)

        self.rds = boto3.client('rds')

    def shutdown_rds(self):
        '''
            Shutdown RDS instances marked with the "autoshutdown" tag.

            Note that AWS takes a snapshot when stopping an RDS instance. This means it can take
            minutes if not hours to shutdown the instance.  While the instance is shutting down it
            is in the 'stopping' state.
        '''

        self.__rds_start_stop(
            filter_state='available',
            msg_tmpl='Stopping DB: %(DBInstanceIdentifier)s',
            boto_method=self.rds.stop_db_instance
        )

        return {
            "message": "shutdown_rds has finished; RDS instances may still be in the process of " +
                       "shutting down",
        }

    def start_rds(self):
        '''
            Start RDS instances marked with the "autoshutdown" tag.
        '''

        self.__rds_start_stop(
            filter_state='stopped',
            msg_tmpl='Starting DB: %(DBInstanceIdentifier)s',
            boto_method=self.rds.start_db_instance
        )

        return {
            "message": "start_rds has finished; RDS instances may still be in the process of " +
                       "starting up",
        }

    def __rds_start_stop(self, **kwargs):
        resp = self.rds.describe_db_instances()
        dbs = filter(
            lambda db: db['DBInstanceStatus'] == kwargs['filter_state'],
            resp['DBInstances']
        )

        for inst in dbs:
            self.log.info(kwargs['msg_tmpl'], inst)
            kwargs['boto_method'](DBInstanceIdentifier=inst['DBInstanceIdentifier'])
