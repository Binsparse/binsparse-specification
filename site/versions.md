---
layout: default
title: Binsparse specification versions
permalink: /versions/
---

# Binsparse specification versions

- [Draft](draft/)
{% if site.data.versions.latest_stable %}
- [Latest stable ({{ site.data.versions.latest_stable }})]({{ site.data.versions.latest_stable }}/)
{% endif %}

## Releases

{% if site.data.versions.releases.size > 0 %}
{% for release in site.data.versions.releases %}
- [{{ release.version }}]({{ release.version }}/){% if release.prerelease %} (prerelease){% endif %}
  ([Bikeshed source]({{ release.version }}/index.bs),
  [HTML]({{ release.version }}/index.html),
  [PDF]({{ release.version }}/index.pdf))
{% endfor %}
{% else %}
No versions have been released yet.
{% endif %}
