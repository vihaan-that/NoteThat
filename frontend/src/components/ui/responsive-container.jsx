import React from "react";

// Utility function for class name merging
const cn = (...classes) => {
  return classes.filter(Boolean).join(" ");
};

const ResponsiveContainer = ({
  children,
  className,
  as: Component = "div",
  useSafeArea = false,
  ...props
}) => {
  return (
    <Component
      className={cn(
        "mx-auto w-full px-4 sm:px-6 md:px-8",
        useSafeArea && "safe-area-inset",
        className
      )}
      {...props}
    >
      {children}
    </Component>
  );
};

export default ResponsiveContainer;
