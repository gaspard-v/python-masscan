const proxy = {
  absolute: true,
  objects: {
    address: {
      type: "string",
    },
    port: {
      type: "integer",
      options: {
        optional: true,
      },
    },
    ip_type: {
      type: "enum",
      values: [
        {
          type: "integer",
          value: 4,
        },
        {
          type: "integer",
          value: 6,
        },
      ],
    },
    methodes: {
      type: "string",
    },
    scan_date: {
      type: "integer",
      options: {
        optional: true,
      },
    },
    commentaire: {
      type: "string",
      optional: true,
    },
  },
};

export default proxy;
