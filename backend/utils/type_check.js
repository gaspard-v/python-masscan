import PropertyRequiredError from "../errors/PropertyRequiredError.js";
import ExtraPropertyError from "../errors/ExtraPropertyError.js";
import PropertyTypeError from "../errors/PropertyTypeError.js";
import PropertyEnumError from "../errors/PropertyEnumError.js";

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
      throw extraProperties.map((property) => new ExtraPropertyError(property));
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
        throw new PropertyRequiredError(propertyName, propertySchema.type);
      } else if (
        propertySchema.type === "string" &&
        typeof propertyValue !== "string"
      ) {
        throw new PropertyTypeError(propertyName, "string");
      } else if (
        propertySchema.type === "integer" &&
        !Number.isInteger(propertyValue)
      ) {
        throw new PropertyTypeError(propertyName, "integer");
      } else if (
        propertySchema.type === "number" &&
        typeof propertyValue !== "number"
      ) {
        throw new PropertyTypeError(propertyName, "number");
      } else if (propertySchema.type === "enum") {
        const allowedValues = propertySchema.values.map((v) => v.value);
        if (!allowedValues.includes(propertyValue)) {
          throw new PropertyEnumError(propertyName, allowedValues);
        }
      }
    } else if (!(propertySchema.options && propertySchema.options.optional)) {
      throw new PropertyRequiredError(propertyName, propertySchema.type);
    }
  }
}
