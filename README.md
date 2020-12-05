# tm2nova

A small utility for converting TextMate language grammars to Nova syntaxes.

**Note**: this is only meant to be a first step. There will almost certainly be issues with the
conversion that you will need to address, a non-exhaustive list of which are outlined below.

### Regular Expression Problems

It seems (unsurprisingly) that there are differences both in the regex parsers themselves, and how
the text is fed into them.

1. Regexes with a `#` may not be escaped. I have an automatic fix for this, but other similar
   escaping issues are likely.
2. TM grammars with begin/end expressions sometimes use `$` as the end match. I suspect this is for
   single-line expressions which a simple Nova `<match>` scope can handle, but I don't convert these
   automatically.

### Highlighting Scope Names

Nova's syntax highlighting scope names do not match, and sometimes there are not direct analogues. I
do a few automatic conversions, but these really need to be (or at least should be) hand-edited.

### Symbols and Folding

Probably the biggest issue with the conversion is that the scopes do not generate symbols. To do this
well (in my limited experience) means really mirroring the grammar of the language in scopes that
capture whole blocks (for example) with proper subscoping. Some of the TM grammars I've seen are more
(or only) focused on syntax highlighting, which is a good first step, but won't get you cool things
like Nova's Symbols panel.
