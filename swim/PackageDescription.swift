#!/usr/bin/env swift

public struct Package {
  public let name: String

  public init(name: String) {
    self.name = name
  }

  public func toJSON() -> String {
    var json = ""
    json += "{"
    json += "  \"name\": \"\(name)\""
    json += "}"
    return json
  }
}

// package

print(package.toJSON())
