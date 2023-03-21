export async function validateObject(schema, object) {
  if (typeof object !== "object" || Array.isArray(object))
    throw new TypeError("Not an object");
  // Vérifier si l'objet a des propriétés supplémentaires
  if (schema.absolute) {
    const schemaProperties = Object.keys(schema.objects);
    const objectProperties = Object.keys(object);
    const extraProperties = objectProperties.filter(
      (prop) => !schemaProperties.includes(prop)
    );
    if (extraProperties.length > 0) {
      throw new TypeError(
        `Object contains extra properties: ${extraProperties.join(", ")}`
      );
    }
  }

  // Vérifier chaque propriété de l'objet
  for (let [propertyName, propertySchema] of Object.entries(schema.objects)) {
    if (propertyName in object) {
      const propertyValue = object[propertyName];
      if (
        propertyValue === undefined &&
        !(propertySchema.options && propertySchema.options.optional)
      ) {
        throw new TypeError(`Missing required property: ${propertyName}`);
      } else if (
        propertySchema.type === "string" &&
        typeof propertyValue !== "string"
      ) {
        throw new TypeError(`Property ${propertyName} should be a string`);
      } else if (
        propertySchema.type === "integer" &&
        !Number.isInteger(propertyValue)
      ) {
        throw new TypeError(`Property ${propertyName} should be an integer`);
      } else if (
        propertySchema.type === "number" &&
        typeof propertyValue !== "number"
      ) {
        throw new TypeError(`Property ${propertyName} should be an number`);
      } else if (propertySchema.type === "enum") {
        const allowedValues = propertySchema.values.map((v) => v.value);
        if (!allowedValues.includes(propertyValue)) {
          throw new TypeError(
            `Property ${propertyName} should be one of: ${allowedValues.join(
              ", "
            )}`
          );
        }
      }
    } else if (!(propertySchema.options && propertySchema.options.optional)) {
      throw new TypeError(`Missing required property: ${propertyName}`);
    }
  }
}
