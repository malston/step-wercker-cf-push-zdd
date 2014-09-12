step-wercker-cf-push
====================

a wercker step to do a Zero Downtime Deploy push to cloud foundry


SAMPLE USAGE:

```
deploy:
  steps:
    - xchapter7x/cf-push:
        cloudfoundry_user_name: $cfuser
        cloudfoundry_user_pass: $cfpass
        cloudfoundry_org: $cforg
        cloudfoundry_space: $cfspace
        cloudfoundry_api_url: $cfurl
        cloudfoundry_app_name: $cfappname
        cloudfoundry_use_manifest: true
```


SUPPORTED ARGUMENTS:
(supports all arguments to 'cf push' CLI)

```
properties:
  cloudfoundry_user_name:
    type: string
    required: true
  cloudfoundry_user_pass:
    type: string
    required: true
  cloudfoundry_org:
    type: string
    required: true
  cloudfoundry_space:
    type: string
    required: true
  cloudfoundry_api_url:
    type: string
    required: true
  cloudfoundry_app_name:
    type: string
    required: true
  cloudfoundry_use_manifest:
    type: boolean
    required: true
  cloudfoundry_buildpack:
    type: string
    required: false
    default: ""
  cloudfoundry_command:
    type: string
    required: false
    default: ""
  cloudfoundry_domain:
    type: string
    required: false
    default: ""
  cloudfoundry_num_instances:
    type: string
    required: false
    default: ""
  cloudfoundry_memory:
    type: string
    required: false
    default: ""
  cloudfoundry_host:
    type: string
    required: false
    default: ""
  cloudfoundry_path:
    type: string
    required: false
    default: ""
  cloudfoundry_stack:
    type: string
    required: false
    default: ""
  cloudfoundry_no_hostname:
    type: boolean
    required: false
    default: false
  cloudfoundry_no_route:
    type: boolean
    required: false
    default: false
  cloudfoundry_no_start:
    type: boolean
    required: false
    default: false
```
