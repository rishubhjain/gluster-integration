import etcd
import subprocess

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.gluster_integration.objects.volume import Volume


class RebalanceRunning(objects.BaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(RebalanceRunning, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Checking if rebalance is running"
                },
                job_id=self.parameters["job_id"],
                flow_id=self.parameters["flow_id"],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )
        try:
            rebal_status = NS._int.client.read(
                'clusters/%s/Volumes/%s/rebal_status' % (
                    NS.tendrl_context.integration_id,
                    self.parameters['Volume.vol_id']
                )
            ).value
            if rebal_status is not None:
                if rebal_status == "in progress":
                    return True
                else:
                    Event(
                        Message(
                            priority="info",
                            publisher=NS.publisher_id,
                            payload={
                                "message": "No rebalance running for volume %s" %
                                self.parameters['Volume.volname']
                            },
                            job_id=self.parameters["job_id"],
                            flow_id=self.parameters["flow_id"],
                            cluster_id=NS.tendrl_context.integration_id,
                        )
                    )
                    return False
            else:
                return False
        except etcd.EtcdKeyNotFound:
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Volume %s not found" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False
