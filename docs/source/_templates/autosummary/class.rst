{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

    {% block attributes %}
    {% if attributes %}
    .. rubric:: {{ _('Attributes') }}

    .. autosummary::
    {% for item in attributes %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}

    {% block methods %}
    {% if methods %}
    .. rubric:: {{ _('Methods') }}

    .. autosummary::
    {% for item in methods if item != '__init__' %}
        ~{{ name }}.{{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}

    |

    .. rubric:: {{ _('Attribute details') }}

    {% for item in attributes %}
    .. autoattribute:: {{ item }}
    {%- endfor %}

    .. rubric:: {{ _('Method details') }}

    {% for item in methods if item != '__init__' %}
    .. automethod:: {{ item }}
    {%- endfor %}