#!/usr/bin/env swift

public struct Package {
  public struct Dependency {
    let url: String

    init(_ url: String) {
      self.url = url
    }

    public static func Package(url url: String, majorVersion: Int) -> Dependency {
      return Dependency(url)
    }

    public static func Package(url url: String, majorVersion: Int, minor: Int) -> Dependency {
      return Dependency(url)
    }

    func toJSON() -> String {
      var json = ""
      json += "{"
      json += "  \"url\": \"\(url)\""
      json += "}"
      return json
    }
  }

  public let name: String
  public let dependencies: [Dependency]
  public let testDependencies: [Dependency]

  public init(name: String, dependencies: [Dependency]? = nil, testDependencies: [Dependency]? = nil) {
    self.name = name
    self.dependencies = dependencies ?? []
    self.testDependencies = testDependencies ?? []
  }

  func toJSON() -> String {
    var json = ""

#if swift(>=3.0)
    let dependenciesJSON = dependencies.map { $0.toJSON() }
    let testDependenciesJSON = testDependencies.map { $0.toJSON() }

    json += "{"
    json += "  \"name\": \"\(name)\","
    json += "  \"dependencies\": ["

    for (index, dependency) in dependenciesJSON.enumerated() {
      json += dependency
      if index + 1 < dependenciesJSON.count {
        json += ","
      }
    }

    json += "  ],"
    json += "  \"test_dependencies\": ["

    for (index, dependency) in testDependenciesJSON.enumerated() {
      json += dependency
      if index + 1 < testDependenciesJSON.count {
        json += ","
      }
    }

    json += "  ]"
    json += "}"
#else
    let dependenciesJSON = dependencies.map { $0.toJSON() }
    let testDependenciesJSON = testDependencies.map { $0.toJSON() }

    json += "{"
    json += "  \"name\": \"\(name)\","
    json += "  \"dependencies\": ["

    for (index, dependency) in dependenciesJSON.enumerate() {
      json += dependency
      if index + 1 < dependenciesJSON.count {
        json += ","
      }
    }

    json += "  ],"
    json += "  \"test_dependencies\": ["

    for (index, dependency) in testDependenciesJSON.enumerate() {
      json += dependency
      if index + 1 < testDependenciesJSON.count {
        json += ","
      }
    }

    json += "  ]"
    json += "}"
#endif
    return json
  }
}

// package

print(package.toJSON())
