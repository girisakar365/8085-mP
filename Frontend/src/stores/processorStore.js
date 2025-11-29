import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';

const DEFAULT_PROCESSOR_STATE = {
  registers: {
    A: '00',
    B: '00',
    C: '00',
    D: '00',
    E: '00',
    H: '00',
    L: '00',
    SP: '0000',
    PC: '0000',
  },
  flags: {
    S: false,
    Z: false,
    AC: false,
    P: false,
    C: false,
  },
  memory: {},
};

export const PROCESSOR_ACTIONS = {
  UPDATE_STATE: 'UPDATE_STATE',
  RESET_STATE: 'RESET_STATE',
  UPDATE_MEMORY: 'UPDATE_MEMORY',
  CLEAR_MEMORY: 'CLEAR_MEMORY',
};

export const processorActions = {
  updateState: (newState) => ({
    type: PROCESSOR_ACTIONS.UPDATE_STATE,
    payload: newState,
  }),

  resetState: () => ({
    type: PROCESSOR_ACTIONS.RESET_STATE,
  }),

  updateMemory: (address, value) => ({
    type: PROCESSOR_ACTIONS.UPDATE_MEMORY,
    payload: { address, value },
  }),

  clearMemory: () => ({
    type: PROCESSOR_ACTIONS.CLEAR_MEMORY,
  }),
};

const useProcessorStore = create(
  subscribeWithSelector((set, get) => ({
    ...DEFAULT_PROCESSOR_STATE,

    dispatch: (action) => {
      const state = get();
      switch (action.type) {
        case PROCESSOR_ACTIONS.UPDATE_STATE:
          
          let memoryData = action.payload.memory || state.memory;
          
          if (Array.isArray(memoryData)) {
            const memoryObj = {};
            memoryData.forEach(item => {
              if (item && typeof item === 'object' && item.address && item.value) {
                memoryObj[String(item.address)] = String(item.value);
              }
            });
            memoryData = memoryObj;
          } else if (memoryData && typeof memoryData === 'object' && memoryData.data) {
            const data = memoryData.data;
            if (Array.isArray(data)) {
              const memoryObj = {};
              data.forEach(item => {
                if (item && typeof item === 'object' && item.address && item.value) {
                  memoryObj[String(item.address)] = String(item.value);
                }
              });
              memoryData = memoryObj;
            } else if (typeof data === 'object') {
              const memoryObj = {};
              Object.entries(data).forEach(([addr, val]) => {
                memoryObj[String(addr)] = String(val);
              });
              memoryData = memoryObj;
            }
          } else if (memoryData && typeof memoryData === 'object') {
            const memoryObj = {};
            Object.entries(memoryData).forEach(([addr, val]) => {
              memoryObj[String(addr)] = String(val);
            });
            memoryData = memoryObj;
          }
          
          set({
            registers: action.payload.registers || state.registers,
            flags: action.payload.flags || state.flags,
            memory: memoryData,
          });
          
          break;

        case PROCESSOR_ACTIONS.RESET_STATE:
          set(DEFAULT_PROCESSOR_STATE);
          break;

        case PROCESSOR_ACTIONS.UPDATE_MEMORY:
          set({
            memory: {
              ...state.memory,
              [action.payload.address]: action.payload.value,
            },
          });
          break;

        case PROCESSOR_ACTIONS.CLEAR_MEMORY:
          set({ memory: {} });
          break;

        default:
          break;
      }
    },
  }))
);

// Selectors
export const processorSelectors = {
  getRegisters: (state) => state.registers,
  getFlags: (state) => state.flags,
  getMemory: (state) => state.memory,
  getRegisterValue: (register) => (state) => state.registers[register],
  getFlagValue: (flag) => (state) => state.flags[flag],
  getMemoryValue: (address) => (state) => state.memory[address],
  getAllState: (state) => ({
    registers: state.registers,
    flags: state.flags,
    memory: state.memory,
  }),

  hasAnyMemory: (state) => Object.keys(state.memory).length > 0,
  getMemorySize: (state) => Object.keys(state.memory).length,
  getActiveFlags: (state) => Object.entries(state.flags)
    .filter(([_, value]) => value)
    .map(([flag, _]) => flag),
};

// Convenience hooks that use selectors
export const useProcessorRegisters = () => useProcessorStore(processorSelectors.getRegisters);
export const useProcessorFlags = () => useProcessorStore(processorSelectors.getFlags);
export const useProcessorMemory = () => useProcessorStore(processorSelectors.getMemory);
export const useProcessorState = () => useProcessorStore(processorSelectors.getAllState);
export const useMemorySize = () => useProcessorStore(processorSelectors.getMemorySize);
export const useActiveFlags = () => useProcessorStore(processorSelectors.getActiveFlags);

// Action hooks
export const useProcessorActions = () => {
  const dispatch = useProcessorStore((state) => state.dispatch);

  return {
    updateState: (newState) => dispatch(processorActions.updateState(newState)),
    resetState: () => dispatch(processorActions.resetState()),
    updateMemory: (address, value) => dispatch(processorActions.updateMemory(address, value)),
    clearMemory: () => dispatch(processorActions.clearMemory()),
  };
};

export default useProcessorStore;
