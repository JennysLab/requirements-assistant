import PageHeader from "../components/common/PageHeader.jsx";
import WizardProgress from "../components/wizard/WizardProgress.jsx";
import LoadingOverlay from "../components/wizard/LoadingOverlay.jsx";
import StepInput from "../components/wizard/StepInput.jsx";
import StepEpics from "../components/wizard/StepEpics.jsx";
import StepRequirements from "../components/wizard/StepRequirements.jsx";
import StepCriteria from "../components/wizard/StepCriteria.jsx";
import StepSummary from "../components/wizard/StepSummary.jsx";
import { useWizard } from "../context/WizardContext.jsx";

const STEPS = { 1: StepInput, 2: StepEpics, 3: StepRequirements, 4: StepCriteria, 5: StepSummary };

export default function WizardPage() {
  const { step, loading, error } = useWizard();
  const Step = STEPS[step];
  return (
    <>
      <PageHeader title="Anforderungen generieren" subtitle="Alles Generierte kannst du bearbeiten, bestätigen oder verwerfen." />
      <WizardProgress />
      {error && <p role="alert" className="mb-4 rounded-md bg-status-reworksoft px-3 py-2 text-sm text-status-rework">{error}</p>}
      <Step />
      {loading && <LoadingOverlay />}
    </>
  );
}
