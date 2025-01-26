{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- set custom_schema_name = custom_schema_name | lower | trim -%}

    {# non-specified schemas go to the default target schema #}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}

    {# prod schemas will go to their custom target schema (mart) #}
    {%- elif target.name == 'prod' -%}
        {{ custom_schema_name }}

    {# beta schemas will go to their default target schema (github_pr_1) #}
    {%- elif target.name == 'beta' -%}
        {{ default_schema }}

    {# dev schemas will go to their default_custom target schema (dbt_mart) #}
    {%- elif target.name == 'dev' -%}
        {{ custom_schema_name }}

        {# Use this if you have more than one person in the project #}
        {# {{ default_schema }}_{{ custom_schema_name }} #}

    {%- endif -%}

{%- endmacro %}
