from cloudshell.shell.core.driver_context import ResourceCommandContext, AutoLoadDetails, AutoLoadAttribute, \
    AutoLoadResource
from collections import defaultdict


class LegacyUtils(object):
    def __init__(self):
        self._datamodel_clss_dict = self.__generate_datamodel_classes_dict()

    def migrate_autoload_details(self, autoload_details, context):
        model_name = context.resource.model
        root_name = context.resource.name
        root = self.__create_resource_from_datamodel(model_name, root_name)
        attributes = self.__create_attributes_dict(autoload_details.attributes)
        self.__attach_attributes_to_resource(attributes, '', root)
        self.__build_sub_resoruces_hierarchy(root, autoload_details.resources, attributes)
        return root

    def __create_resource_from_datamodel(self, model_name, res_name):
        return self._datamodel_clss_dict[model_name](res_name)

    def __create_attributes_dict(self, attributes_lst):
        d = defaultdict(list)
        for attribute in attributes_lst:
            d[attribute.relative_address].append(attribute)
        return d

    def __build_sub_resoruces_hierarchy(self, root, sub_resources, attributes):
        d = defaultdict(list)
        for resource in sub_resources:
            splitted = resource.relative_address.split('/')
            parent = '' if len(splitted) == 1 else resource.relative_address.rsplit('/', 1)[0]
            rank = len(splitted)
            d[rank].append((parent, resource))

        self.__set_models_hierarchy_recursively(d, 1, root, '', attributes)

    def __set_models_hierarchy_recursively(self, dict, rank, manipulated_resource, resource_relative_addr, attributes):
        if rank not in dict: # validate if key exists
            pass

        for (parent, resource) in dict[rank]:
            if parent == resource_relative_addr:
                sub_resource = self.__create_resource_from_datamodel(
                    resource.model.replace(' ', ''),
                    resource.name)
                self.__attach_attributes_to_resource(attributes, resource.relative_address, sub_resource)
                manipulated_resource.add_sub_resource(
                    self.__slice_parent_from_relative_path(parent, resource.relative_address), sub_resource)
                self.__set_models_hierarchy_recursively(
                    dict,
                    rank + 1,
                    sub_resource,
                    resource.relative_address,
                    attributes)

    def __attach_attributes_to_resource(self, attributes, curr_relative_addr, resource):
        for attribute in attributes[curr_relative_addr]:
            setattr(resource, attribute.attribute_name.lower().replace(' ', '_'), attribute.attribute_value)
        del attributes[curr_relative_addr]

    def __slice_parent_from_relative_path(self, parent, relative_addr):
        if parent is '':
            return relative_addr
        return relative_addr[len(parent) + 1:] # + 1 because we want to remove the seperator also

    def __generate_datamodel_classes_dict(self):
        return dict(self.__collect_generated_classes())

    def __collect_generated_classes(self):
        import sys, inspect
        return inspect.getmembers(sys.modules[__name__], inspect.isclass)


class Sentry4G2Pdu(object):
    def __init__(self, name):
        """
        
        """
        self.attributes = {}
        self.resources = {}
        self._cloudshell_model_name = 'Sentry4G2Pdu'
        self._name = name

    def add_sub_resource(self, relative_path, sub_resource):
        self.resources[relative_path] = sub_resource

    @classmethod
    def create_from_context(cls, context):
        """
        Creates an instance of NXOS by given context
        :param context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :type context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :return:
        :rtype Sentry4G2Pdu
        """
        result = Sentry4G2Pdu(name=context.resource.name)
        for attr in context.resource.attributes:
            result.attributes[attr] = context.resource.attributes[attr]
        return result

    def create_autoload_details(self, relative_path=''):
        """
        :param relative_path:
        :type relative_path: str
        :return
        """
        resources = [AutoLoadResource(model=self.resources[r].cloudshell_model_name,
            name=self.resources[r].name,
            relative_address=self._get_relative_path(r, relative_path))
            for r in self.resources]
        attributes = [AutoLoadAttribute(relative_path, a, self.attributes[a]) for a in self.attributes]
        autoload_details = AutoLoadDetails(resources, attributes)
        for r in self.resources:
            curr_path = relative_path + '/' + r if relative_path else r
            curr_auto_load_details = self.resources[r].create_autoload_details(curr_path)
            autoload_details = self._merge_autoload_details(autoload_details, curr_auto_load_details)
        return autoload_details

    def _get_relative_path(self, child_path, parent_path):
        """
        Combines relative path
        :param child_path: Path of a model within it parent model, i.e 1
        :type child_path: str
        :param parent_path: Full path of parent model, i.e 1/1. Might be empty for root model
        :type parent_path: str
        :return: Combined path
        :rtype str
        """
        return parent_path + '/' + child_path if parent_path else child_path

    @staticmethod
    def _merge_autoload_details(autoload_details1, autoload_details2):
        """
        Merges two instances of AutoLoadDetails into the first one
        :param autoload_details1:
        :type autoload_details1: AutoLoadDetails
        :param autoload_details2:
        :type autoload_details2: AutoLoadDetails
        :return:
        :rtype AutoLoadDetails
        """
        for attribute in autoload_details2.attributes:
            autoload_details1.attributes.append(attribute)
        for resource in autoload_details2.resources:
            autoload_details1.resources.append(resource)
        return autoload_details1

    @property
    def cloudshell_model_name(self):
        """
        Returns the name of the Cloudshell model
        :return:
        """
        return 'Sentry4G2Pdu'

    @property
    def serial_number(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.Serial Number'] if 'Sentry4G2Pdu.Serial Number' in self.attributes else None

    @serial_number.setter
    def serial_number(self, value):
        """
        Items Factory Serial Number
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.Serial Number'] = value

    @property
    def firmware_version(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.Firmware Version'] if 'Sentry4G2Pdu.Firmware Version' in self.attributes else None

    @firmware_version.setter
    def firmware_version(self, value):
        """
        Current Firmware on the device
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.Firmware Version'] = value

    @property
    def hardware_details(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.Hardware Details'] if 'Sentry4G2Pdu.Hardware Details' in self.attributes else None

    @hardware_details.setter
    def hardware_details(self, value):
        """
        Short desription of the hardware configuration for this device
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.Hardware Details'] = value

    @property
    def user(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.User'] if 'Sentry4G2Pdu.User' in self.attributes else None

    @user.setter
    def user(self, value):
        """
        User with administrative privileges
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.User'] = value

    @property
    def password(self):
        """
        :rtype: string
        """
        return self.attributes['Sentry4G2Pdu.Password'] if 'Sentry4G2Pdu.Password' in self.attributes else None

    @password.setter
    def password(self, value):
        """
        
        :type value: string
        """
        self.attributes['Sentry4G2Pdu.Password'] = value

    @property
    def enable_password(self):
        """
        :rtype: string
        """
        return self.attributes['Sentry4G2Pdu.Enable Password'] if 'Sentry4G2Pdu.Enable Password' in self.attributes else None

    @enable_password.setter
    def enable_password(self, value):
        """
        The enable password is required by some CLI protocols such as Telnet and is required according to the device configuration.
        :type value: string
        """
        self.attributes['Sentry4G2Pdu.Enable Password'] = value

    @property
    def power_management(self):
        """
        :rtype: bool
        """
        return self.attributes['Sentry4G2Pdu.Power Management'] if 'Sentry4G2Pdu.Power Management' in self.attributes else None

    @power_management.setter
    def power_management(self, value=True):
        """
        Used by the power management orchestration, if enabled, to determine whether to automatically manage the device power status. Enabled by default.
        :type value: bool
        """
        self.attributes['Sentry4G2Pdu.Power Management'] = value

    @property
    def contact_name(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.Contact Name'] if 'Sentry4G2Pdu.Contact Name' in self.attributes else None

    @contact_name.setter
    def contact_name(self, value):
        """
        The name of a contact registered in the device.
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.Contact Name'] = value

    @property
    def sessions_concurrency_limit(self):
        """
        :rtype: float
        """
        return self.attributes['Sentry4G2Pdu.Sessions Concurrency Limit'] if 'Sentry4G2Pdu.Sessions Concurrency Limit' in self.attributes else None

    @sessions_concurrency_limit.setter
    def sessions_concurrency_limit(self, value='1'):
        """
        The maximum number of concurrent sessions that the driver will open to the device. Default is 1 (no concurrency).
        :type value: float
        """
        self.attributes['Sentry4G2Pdu.Sessions Concurrency Limit'] = value

    @property
    def snmp_read_community(self):
        """
        :rtype: string
        """
        return self.attributes['Sentry4G2Pdu.SNMP Read Community'] if 'Sentry4G2Pdu.SNMP Read Community' in self.attributes else None

    @snmp_read_community.setter
    def snmp_read_community(self, value):
        """
        The SNMP Read-Only Community String is like a password. It is sent along with each SNMP Get-Request and allows (or denies) access to device.
        :type value: string
        """
        self.attributes['Sentry4G2Pdu.SNMP Read Community'] = value

    @property
    def snmp_write_community(self):
        """
        :rtype: string
        """
        return self.attributes['Sentry4G2Pdu.SNMP Write Community'] if 'Sentry4G2Pdu.SNMP Write Community' in self.attributes else None

    @snmp_write_community.setter
    def snmp_write_community(self, value):
        """
        The SNMP Write Community String is like a password. It is sent along with each SNMP Set-Request and allows (or denies) chaning MIBs values.
        :type value: string
        """
        self.attributes['Sentry4G2Pdu.SNMP Write Community'] = value

    @property
    def snmp_v3_user(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.SNMP V3 User'] if 'Sentry4G2Pdu.SNMP V3 User' in self.attributes else None

    @snmp_v3_user.setter
    def snmp_v3_user(self, value):
        """
        Relevant only in case SNMP V3 is in use.
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.SNMP V3 User'] = value

    @property
    def snmp_v3_password(self):
        """
        :rtype: string
        """
        return self.attributes['Sentry4G2Pdu.SNMP V3 Password'] if 'Sentry4G2Pdu.SNMP V3 Password' in self.attributes else None

    @snmp_v3_password.setter
    def snmp_v3_password(self, value):
        """
        Relevant only in case SNMP V3 is in use.
        :type value: string
        """
        self.attributes['Sentry4G2Pdu.SNMP V3 Password'] = value

    @property
    def snmp_v3_private_key(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.SNMP V3 Private Key'] if 'Sentry4G2Pdu.SNMP V3 Private Key' in self.attributes else None

    @snmp_v3_private_key.setter
    def snmp_v3_private_key(self, value):
        """
        Relevant only in case SNMP V3 is in use.
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.SNMP V3 Private Key'] = value

    @property
    def snmp_version(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.SNMP Version'] if 'Sentry4G2Pdu.SNMP Version' in self.attributes else None

    @snmp_version.setter
    def snmp_version(self, value=''):
        """
        The version of SNMP to use. Possible values are v1, v2c and v3.
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.SNMP Version'] = value

    @property
    def enable_snmp(self):
        """
        :rtype: bool
        """
        return self.attributes['Sentry4G2Pdu.Enable SNMP'] if 'Sentry4G2Pdu.Enable SNMP' in self.attributes else None

    @enable_snmp.setter
    def enable_snmp(self, value=True):
        """
        If set to True and SNMP isn???t enabled yet in the device the Shell will automatically enable SNMP in the device when Autoload command is called. SNMP must be enabled on the device for the Autoload command to run successfully. True by default.
        :type value: bool
        """
        self.attributes['Sentry4G2Pdu.Enable SNMP'] = value

    @property
    def disable_snmp(self):
        """
        :rtype: bool
        """
        return self.attributes['Sentry4G2Pdu.Disable SNMP'] if 'Sentry4G2Pdu.Disable SNMP' in self.attributes else None

    @disable_snmp.setter
    def disable_snmp(self, value=False):
        """
        If set to True SNMP will be disabled automatically by the Shell after the Autoload command execution is completed. False by default.
        :type value: bool
        """
        self.attributes['Sentry4G2Pdu.Disable SNMP'] = value

    @property
    def console_server_ip_address(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.Console Server IP Address'] if 'Sentry4G2Pdu.Console Server IP Address' in self.attributes else None

    @console_server_ip_address.setter
    def console_server_ip_address(self, value):
        """
        The IP address of the console server, in IPv4 format.
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.Console Server IP Address'] = value

    @property
    def console_user(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.Console User'] if 'Sentry4G2Pdu.Console User' in self.attributes else None

    @console_user.setter
    def console_user(self, value):
        """
        
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.Console User'] = value

    @property
    def console_port(self):
        """
        :rtype: float
        """
        return self.attributes['Sentry4G2Pdu.Console Port'] if 'Sentry4G2Pdu.Console Port' in self.attributes else None

    @console_port.setter
    def console_port(self, value):
        """
        The port on the console server, usually TCP port, which the device is associated with.
        :type value: float
        """
        self.attributes['Sentry4G2Pdu.Console Port'] = value

    @property
    def console_password(self):
        """
        :rtype: string
        """
        return self.attributes['Sentry4G2Pdu.Console Password'] if 'Sentry4G2Pdu.Console Password' in self.attributes else None

    @console_password.setter
    def console_password(self, value):
        """
        
        :type value: string
        """
        self.attributes['Sentry4G2Pdu.Console Password'] = value

    @property
    def cli_connection_type(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.CLI Connection Type'] if 'Sentry4G2Pdu.CLI Connection Type' in self.attributes else None

    @cli_connection_type.setter
    def cli_connection_type(self, value='Auto'):
        """
        The CLI connection type that will be used by the driver. Possible values are Auto, Console, SSH, Telnet and TCP. If Auto is selected the driver will choose the available connection type automatically. Default value is Auto.
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.CLI Connection Type'] = value

    @property
    def cli_tcp_port(self):
        """
        :rtype: float
        """
        return self.attributes['Sentry4G2Pdu.CLI TCP Port'] if 'Sentry4G2Pdu.CLI TCP Port' in self.attributes else None

    @cli_tcp_port.setter
    def cli_tcp_port(self, value):
        """
        TCP Port to user for CLI connection. If kept empty a default CLI port will be used based on the chosen protocol, for example Telnet will use port 23.
        :type value: float
        """
        self.attributes['Sentry4G2Pdu.CLI TCP Port'] = value

    @property
    def backup_location(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.Backup Location'] if 'Sentry4G2Pdu.Backup Location' in self.attributes else None

    @backup_location.setter
    def backup_location(self, value):
        """
        Used by the save/restore orchestration to determine where backups should be saved.
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.Backup Location'] = value

    @property
    def backup_type(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.Backup Type'] if 'Sentry4G2Pdu.Backup Type' in self.attributes else None

    @backup_type.setter
    def backup_type(self, value='File System'):
        """
        Supported protocols for saving and restoring of configuration and firmware files. Possible values are 'File System' 'FTP' and 'TFTP'. Default value is 'File System'.
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.Backup Type'] = value

    @property
    def backup_user(self):
        """
        :rtype: str
        """
        return self.attributes['Sentry4G2Pdu.Backup User'] if 'Sentry4G2Pdu.Backup User' in self.attributes else None

    @backup_user.setter
    def backup_user(self, value):
        """
        Username for the storage server used for saving and restoring of configuration and firmware files.
        :type value: str
        """
        self.attributes['Sentry4G2Pdu.Backup User'] = value

    @property
    def backup_password(self):
        """
        :rtype: string
        """
        return self.attributes['Sentry4G2Pdu.Backup Password'] if 'Sentry4G2Pdu.Backup Password' in self.attributes else None

    @backup_password.setter
    def backup_password(self, value):
        """
        Password for the storage server used for saving and restoring of configuration and firmware files.
        :type value: string
        """
        self.attributes['Sentry4G2Pdu.Backup Password'] = value

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        
        :type value: str
        """
        self._name = value

    @property
    def cloudshell_model_name(self):
        """
        :rtype: str
        """
        return self._cloudshell_model_name

    @cloudshell_model_name.setter
    def cloudshell_model_name(self, value):
        """
        
        :type value: str
        """
        self._cloudshell_model_name = value

    @property
    def system_name(self):
        """
        :rtype: str
        """
        return self.attributes['CS_PDU.System Name'] if 'CS_PDU.System Name' in self.attributes else None

    @system_name.setter
    def system_name(self, value):
        """
        A unique identifier for the device, if exists in the device terminal/os.
        :type value: str
        """
        self.attributes['CS_PDU.System Name'] = value

    @property
    def vendor(self):
        """
        :rtype: str
        """
        return self.attributes['CS_PDU.Vendor'] if 'CS_PDU.Vendor' in self.attributes else None

    @vendor.setter
    def vendor(self, value=''):
        """
        The name of the device manufacture.
        :type value: str
        """
        self.attributes['CS_PDU.Vendor'] = value

    @property
    def location(self):
        """
        :rtype: str
        """
        return self.attributes['CS_PDU.Location'] if 'CS_PDU.Location' in self.attributes else None

    @location.setter
    def location(self, value=''):
        """
        The device physical location identifier. For example Lab1/Floor2/Row5/Slot4.
        :type value: str
        """
        self.attributes['CS_PDU.Location'] = value

    @property
    def model(self):
        """
        :rtype: str
        """
        return self.attributes['CS_PDU.Model'] if 'CS_PDU.Model' in self.attributes else None

    @model.setter
    def model(self, value=''):
        """
        The device model. This information is typically used for abstract resource filtering.
        :type value: str
        """
        self.attributes['CS_PDU.Model'] = value

    @property
    def model_name(self):
        """
        :rtype: str
        """
        return self.attributes['CS_PDU.Model Name'] if 'CS_PDU.Model Name' in self.attributes else None

    @model_name.setter
    def model_name(self, value=''):
        """
        The catalog name of the device model. This attribute will be displayed in CloudShell instead of the CloudShell model.
        :type value: str
        """
        self.attributes['CS_PDU.Model Name'] = value


class PowerSocket(object):
    def __init__(self, name):
        """
        
        """
        self.attributes = {}
        self.resources = {}
        self._cloudshell_model_name = 'Sentry4G2Pdu.PowerSocket'
        self._name = name

    def add_sub_resource(self, relative_path, sub_resource):
        self.resources[relative_path] = sub_resource

    @classmethod
    def create_from_context(cls, context):
        """
        Creates an instance of NXOS by given context
        :param context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :type context: cloudshell.shell.core.driver_context.ResourceCommandContext
        :return:
        :rtype PowerSocket
        """
        result = PowerSocket(name=context.resource.name)
        for attr in context.resource.attributes:
            result.attributes[attr] = context.resource.attributes[attr]
        return result

    def create_autoload_details(self, relative_path=''):
        """
        :param relative_path:
        :type relative_path: str
        :return
        """
        resources = [AutoLoadResource(model=self.resources[r].cloudshell_model_name,
            name=self.resources[r].name,
            relative_address=self._get_relative_path(r, relative_path))
            for r in self.resources]
        attributes = [AutoLoadAttribute(relative_path, a, self.attributes[a]) for a in self.attributes]
        autoload_details = AutoLoadDetails(resources, attributes)
        for r in self.resources:
            curr_path = relative_path + '/' + r if relative_path else r
            curr_auto_load_details = self.resources[r].create_autoload_details(curr_path)
            autoload_details = self._merge_autoload_details(autoload_details, curr_auto_load_details)
        return autoload_details

    def _get_relative_path(self, child_path, parent_path):
        """
        Combines relative path
        :param child_path: Path of a model within it parent model, i.e 1
        :type child_path: str
        :param parent_path: Full path of parent model, i.e 1/1. Might be empty for root model
        :type parent_path: str
        :return: Combined path
        :rtype str
        """
        return parent_path + '/' + child_path if parent_path else child_path

    @staticmethod
    def _merge_autoload_details(autoload_details1, autoload_details2):
        """
        Merges two instances of AutoLoadDetails into the first one
        :param autoload_details1:
        :type autoload_details1: AutoLoadDetails
        :param autoload_details2:
        :type autoload_details2: AutoLoadDetails
        :return:
        :rtype AutoLoadDetails
        """
        for attribute in autoload_details2.attributes:
            autoload_details1.attributes.append(attribute)
        for resource in autoload_details2.resources:
            autoload_details1.resources.append(resource)
        return autoload_details1

    @property
    def cloudshell_model_name(self):
        """
        Returns the name of the Cloudshell model
        :return:
        """
        return 'PowerSocket'

    @property
    def name(self):
        """
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        
        :type value: str
        """
        self._name = value

    @property
    def cloudshell_model_name(self):
        """
        :rtype: str
        """
        return self._cloudshell_model_name

    @cloudshell_model_name.setter
    def cloudshell_model_name(self, value):
        """
        
        :type value: str
        """
        self._cloudshell_model_name = value

    @property
    def model_name(self):
        """
        :rtype: str
        """
        return self.attributes['CS_PowerSocket.Model Name'] if 'CS_PowerSocket.Model Name' in self.attributes else None

    @model_name.setter
    def model_name(self, value=''):
        """
        The catalog name of the device model. This attribute will be displayed in CloudShell instead of the CloudShell model.
        :type value: str
        """
        self.attributes['CS_PowerSocket.Model Name'] = value



