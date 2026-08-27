# Binsparse: A Binary Sparse Matrix and Tensor Format Specification
Binsparse is binary storage format for storing sparse matrices and tensors to disk.

Minutes from our meetings are available [here](https://hackmd.io/0qzK4fJlQp-78t067yiYsA?view) (see also: [previous minutes](minutes)).

## Specification

[View Latest Spec](https://binsparse.github.io/binsparse-specification/)

### Editing

The working version of the specification can be found under `spec/latest/index.bs`.

The spec is written in [bikeshed](https://github.com/tabatkins/bikeshed) – a variant of markdown.
To render the spec locally:

* Install bikeshed (ideally in an isolated environment): `pipx install bikeshed`
* Call `bikeshed spec spec/latest/index.bs`

To render the spec online, see [api.csswg.org](https://api.csswg.org/bikeshed/),
or use the following commands:

```
cd binsparse-specification/spec/latest
curl https://api.csswg.org/bikeshed/ -F file=@index.bs > index.html
```

Rendered versions will generated for pull requests.
