export const proxy_t = {
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
    },
    commentaire: {
      type: "string",
      options: {
        optional: true,
      },
    },
  },
};

export const default_proxy = {
  address: "",
  port: 0,
  ip_type: 4,
  methodes: "",
  scan_date: 0,
  commentaire: null,
};
