import os
import torch
from transformers import AutoConfig
from transformers.modeling_outputs import BaseModelOutput
from transformers.modeling_utils import PreTrainedModel


class CompiledModel(PreTrainedModel):

    @classmethod
    def from_model(cls, model):
        compiled_model = cls(model.config)
        compiled_model.model = model.model

        return compiled_model

    # def prepare_inputs_for_generation(
    #         self,
    #         input_ids,
    #         encoder_outputs=None,
    #         attention_mask=None,
    #         **kwargs,
    # ):
    #     # Pad the inputs for Neuron
    #     current_length = input_ids.shape[1]
    #     pad_size = self.config.max_length - current_length
    #     return dict(
    #         input_ids=F.pad(input_ids, (0, pad_size)),
    #         attention_mask=attention_mask,
    #         encoder_outputs=encoder_outputs.last_hidden_state,
    #         current_length=torch.tensor(current_length - 1),
    #     )

    # def get_encoder(self):
    #     def encode(input_ids, attention_mask, **kwargs):
    #         output, = self.encoder(input_ids, attention_mask)
    #         return BaseModelOutput(
    #             last_hidden_state=output,
    #         )
    #     return encode

    def forward(self, input_ids, attention_mask, current_length, **kwargs):
        logits = self.model(input_ids, attention_mask)
        return Seq2SeqLMOutput(logits=logits)

    @property
    def device(self):  # Attribute required by beam search
        return torch.device('cpu')

    def save_pretrained(self, directory):
        if os.path.isfile(directory):
            print(f"Provided path ({directory}) should be a directory, not a file")
            return
        os.makedirs(directory, exist_ok=True)
        torch.jit.save(self.model, os.path.join(directory, 'model.pt'))
        #torch.jit.save(self.decoder, os.path.join(directory, 'decoder.pt'))
        self.config.save_pretrained(directory)

    @classmethod
    def from_pretrained(cls, directory):
        config = AutoConfig.from_pretrained(directory)
        compiled_model = cls(config)
        compiled_model.model = torch.jit.load(os.path.join(directory, 'model.pt'))
        #setattr(obj.encoder, 'main_input_name', 'input_ids')  # Attribute required by beam search
        return compiled_model