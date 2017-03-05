# pylint: disable=missing-docstring,invalid-name
# pylint: disable=redefined-builtin,wildcard-import,unused-wildcard-import
from ansible.module_utils.basic import *

def read_mail(module, name, erase, max_length):
    f = open(name, 'r')
    try:
        raw_mail = f.read().split('\n')
    finally:
        f.close()
    mail = []
    for line in raw_mail:
        if line.startswith('From '):
            mail.append(line)
        elif len(mail) > 0:
            if len(mail[-1]) + len(line) >= max_length:
                mail.append(line)
            else:
                mail[-1] += '\n{}'.format(line)
    changed = True if len(mail) > 0 else False
    if erase:
        f = open(name, 'w')
        try:
            f.write('')
        finally:
            f.close()
    return {'changed': changed, 'e-mails': mail, 'name': name}

def main():
    argument_spec = {
        'name': {'required': True},
        'erase': {'default': False, 'type': 'bool'},
        'max_length': {'default': 4096, 'type': 'int'},
    }
    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    name = module.params['name']
    erase = module.params['erase']
    max_length = module.params['max_length']
    result = read_mail(module, name, erase, max_length)
    module.exit_json(**result)

if __name__ == '__main__':
    main()
