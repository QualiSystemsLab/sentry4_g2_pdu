# from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
# from cloudshell.shell.core.driver_context import InitCommandContext, ResourceCommandContext, AutoLoadResource, \
#     AutoLoadAttribute, AutoLoadDetails, CancellationContext
#from data_model import *  # run 'shellfoundry generate' to generate data model classes

from sentry.pm_pdu_handler import PmPduHandler
from cloudshell.power.pdu.power_resource_driver_interface import PowerResourceDriverInterface
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.context import AutoLoadDetails, InitCommandContext, ResourceCommandContext
from log_helper import LogHelper
from data_model import *
import cloudshell.api.cloudshell_api as cs_api


class SentryPduDriver (ResourceDriverInterface):

    def __init__(self):
        """
        ctor must be without arguments, it is created with reflection at run time
        """
        pass

    def initialize(self, context):
        """
        Initialize the driver session, this function is called everytime a new instance of the driver is created
        This is a good place to load and cache the driver configuration, initiate sessions etc.
        :param InitCommandContext context: the context the command runs on
        """
        pass

    def cleanup(self):
        """
        Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """
        pass

    def get_inventory(self, context):
        """

        :param ResourceCommandContext context:
        :return:
        """
        resource = Sentry4G2Pdu.create_from_context(context)
        read = resource.snmp_read_community
        write = resource.snmp_write_community
        handler = PmPduHandler(context,
                               self._decrypt_password(context, read),
                               self._decrypt_password(context, write)
                               )

        return handler.get_inventory()

    def PowerCycle(self, context, ports, delay):

        try:
            if delay < 8:
                s_delay = 8
            else:
                s_delay = delay

            float(s_delay)
        except ValueError:
            raise Exception('Delay must be a numeric value')

        resource = Sentry4G2Pdu.create_from_context(context)
        read = resource.snmp_read_community
        write = resource.snmp_write_community
        handler = PmPduHandler(context,
                               self._decrypt_password(context, read),
                               self._decrypt_password(context, write)
                               )

        return handler.power_cycle(ports, float(delay), self._find_connected_to(context, ports))

    def PowerOff(self, context, ports):
        """

        :param ResourceCommandContext context:
        :param ports:
        :return:
        """
        resource = Sentry4G2Pdu.create_from_context(context)
        read = resource.snmp_read_community
        write = resource.snmp_write_community
        handler = PmPduHandler(context,
                               self._decrypt_password(context, read),
                               self._decrypt_password(context, write)
                               )

        return handler.power_off(ports, self._find_connected_to(context, ports))

    def PowerOn(self, context, ports):
        """

        :param ResourceCommandContext context:
        :param ports:
        :return:

        """
        resource = Sentry4G2Pdu.create_from_context(context)
        read = resource.snmp_read_community
        write = resource.snmp_write_community
        handler = PmPduHandler(context,
                               self._decrypt_password(context, read),
                               self._decrypt_password(context, write),

                               )

        return handler.power_on(ports, self._find_connected_to(context, ports))

    def _decrypt_password(self, context, input):
        """
        A simple example function
        :param str input: password string to decode
        :return str
        """
        session = cs_api.CloudShellAPISession(host=context.connectivity.server_address,
                                              token_id=context.connectivity.admin_auth_token,
                                              domain='Global')

        return session.DecryptPassword(input).Value

    def _find_connected_to(self, context, ports=[]):

        session = cs_api.CloudShellAPISession(host=context.connectivity.server_address,
                                              token_id=context.connectivity.admin_auth_token,
                                              domain='Global')
        dut_list = []

        for port in ports:
            res = session.FindResources(resourceModel='Sentry4G2Pdu.PowerSocket', resourceAddress=port).Resources
            for r in res:
                if port == r.FullAddress:
                    con = session.GetResourceDetails(r.FullName).Connections
                    for c in con:
                        dut_list.append(c.FullPath.split('/')[-2])
        return dut_list

if __name__ == "__main__":
    import mock
    from cloudshell.shell.core.driver_context import CancellationContext
    shell_name = "Sentry4G2Pdu"

    cancellation_context = mock.create_autospec(CancellationContext)
    context = mock.create_autospec(ResourceCommandContext)
    context.resource = mock.MagicMock()
    context.reservation = mock.MagicMock()
    context.connectivity = mock.MagicMock()
    context.reservation.reservation_id = "<Reservation ID>"
#    context.resource.address = "10.11.100.251"  # Sentry 4
    context.resource.address = "10.16.145.249"  # Sentry 3
    context.resource.name = "Debug_Sentry4"
    context.resource.attributes = dict()
    context.resource.attributes["{}.User".format(shell_name)] = "admn"
    context.resource.attributes["{}.Password".format(shell_name)] = "admn"
    context.resource.attributes["{}.SNMP Read Community".format(shell_name)] = "public"
    context.resource.attributes["{}.SNMP Write Community".format(shell_name)] = "private"

    driver = SentryPduDriver()
    # print driver.run_custom_command(context, custom_command="sh run", cancellation_context=cancellation_context)
    driver.initialize(context)
    result = driver.get_inventory(context)

    print "done"