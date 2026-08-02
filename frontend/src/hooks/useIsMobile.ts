import useMediaQuery from "./useMediaQuery";

export default function useIsMobile(breakpoint = 768) {
  const query = `(max-width: ${breakpoint - 1}px)`;
  return useMediaQuery(query);
}
