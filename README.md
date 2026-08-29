# Binsparse: A Binary Sparse Matrix and Tensor Format Specification
Binsparse is binary storage format for storing sparse matrices and tensors to disk.

Minutes from our meetings are available [here](https://hackmd.io/0qzK4fJlQp-78t067yiYsA?view) (see also: [previous minutes](minutes)).

## Specification

[View Latest Spec](https://binsparse.github.io/binsparse-specification/)

### Editing

The working version of the specification can be found under `spec/draft/index.bs`.

The spec is written in [bikeshed](https://github.com/tabatkins/bikeshed) – a variant of markdown.
To render the spec locally:

* Install bikeshed (ideally in an isolated environment): `pipx install bikeshed`
* Call `bikeshed spec spec/draft/index.bs`

To render the spec online, see [api.csswg.org](https://api.csswg.org/bikeshed/),
or use the following commands:

```
cd binsparse-specification/spec/draft
curl https://api.csswg.org/bikeshed/ -F file=@index.bs > index.html
```

Rendered versions will be generated for pull requests.

### Releasing

Specification releases use [Semantic Versioning](https://semver.org/). Run the
`Release` workflow from `main`. The workflow reads the version
from the current draft, builds the specification, publishes a corresponding tag
such as `v0.1.0`, and creates a GitHub Release containing the Bikeshed source,
HTML, and PDF artifacts.

The specification's current version is defined once by the `SPECVERSION` Bikeshed
text macro at the top of `spec/draft/index.bs`. Release versions must match it.
