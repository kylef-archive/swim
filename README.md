# Swim

Swim is a simple build system for Swift. Swim allows you to build and test your
Swift code.

## Goals

- swim is compatible with multiple versions of Swift (2.x, 3.x, etc)
- swim allows you to test your Swift project with third-party testing
  frameworks such as [Spectre](https://github.com/kylef/Spectre) and
  [Ploughman](https://github.com/kylef/Ploughman).
- swim is compatible with common Swift Package Manager libraries.
- swim is easy to install (does not depend on Swift)

### Why not just use Swift Package Manager?

The Swift Package Manager has great potential, however right now it is missing
the ability to use third-party testing libraries along with working easily on
multiple versions of Swift like Swift 2.2.

## Installation

```shell
$ pip install swim
```

## Usage

### Building

You can use `swim` to build your project, providing the source is in `Sources/`
and test files are in `Tests`. You may define your dependencies in
`Package.swift` exactly like you would for the Swift Package Manager.

```shell
$ swim build
```

### Testing

You can integrate swim with any testing library of your choice, you will need
to create a `main.swift` file inside `Tests` which runs your tests.

```shell
$ swim test
```

##### `Tests/main.swift`

```swift
import Spectre


describe("a string") {
  $0.it("can be compared to another string") {
    try expect("Kyle") == "Kyle"
  }
}
```

### Swift Package Manager Compatibility

`swim` is *mostly* compatible with the Swift Package Manager, however many
features are missing. swim doesn't aim to be a complete drop-in replacement for
Swift Package Manager and only supports a subset of features. This covers most
common features.

Current known limitations:

- Only Swift sources are supported.
- Dependencies are not locked to versions you specify in your `Package.swift`
  file.
- Only one level of source files.
- You may only define `name`, `dependencies` and `testDependencies` in
  `Package.swift` files.

Pull requests are highly welcome.

## swim on Travis CI

You can use `swim` on Travis CI to test against multiple versions of Swift, on
multiple platforms.

```yaml
install:
- if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then sudo python -m ensurepip; fi
- sudo pip install swim
```

It works great on conjunction with [swiftenv](https://swiftenv.fuller.li/).

```yaml
os:
  - linux
  - osx
env:
  - SWIFT_VERSION=2.2
  - SWIFT_VERSION=3.0-preview-1-SNAPSHOT-2016-05-31-a
language: generic
sudo: required
dist: trusty
osx_image: xcode7.3
install:
  - eval "$(curl -sL https://gist.githubusercontent.com/kylef/5c0475ff02b7c7671d2a/raw/9f442512a46d7a2af7b850d65a7e9bd31edfb09b/swiftenv-install.sh)"
  - if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then sudo python -m ensurepip; fi
  - sudo pip install swim
script:
  - swim test
```
