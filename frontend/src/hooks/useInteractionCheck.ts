import { useMutation, useQueryClient } from "@tanstack/react-query";
import { runInteractionCheck } from "@/api/client";

export function useInteractionCheck(patientId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => runInteractionCheck(patientId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["medications", patientId] });
    },
  });
}
