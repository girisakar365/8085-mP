// Processor Feature - Components
export { default as ProcessorState } from './components/ProcessorState';

// Processor Feature - Store
export {
  default as useProcessorStore,
  useProcessorRegisters,
  useProcessorFlags,
  useProcessorMemory,
  useProcessorState,
  useMemorySize,
  useActiveFlags,
  useProcessorActions,
  processorSelectors,
  processorActions,
  PROCESSOR_ACTIONS,
} from './stores/processorStore';
