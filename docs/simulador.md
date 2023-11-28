---
hide:
  - toc
---

# Controle de Trajetória de Foguetes D'água

## Simular Voos

<div style="text-align: center;">

  <form>
    <div style="display: flex; justify-content: space-around;">

      <div style="display: flex; flex-direction: column; text-align: center; margin-bottom: 10px; width: 120px;">
        <input type="number" id="pressao" name="pressao" style="border: 1px solid black; border-radius: 25px; height: 30px; text-align: center;" required>
        <label for="pressao" style="font-style: italic; opacity: 0.7;">Pressão</label>
      </div>

      <div style="display: flex; flex-direction: column; text-align: center; margin-bottom: 10px; width: 120px;">
        <input type="number" id="volume" name="volume" style="border: 1px solid black; border-radius: 25px; height: 30px; text-align: center;" required>
        <label for="volume" style="font-style: italic; opacity: 0.7; word-wrap: break-word;">Volume D'água</label>
      </div>

      <div style="display: flex; flex-direction: column; text-align: center; margin-bottom: 10px; width: 120px;">
        <input type="number" id="angulo" name="angulo" style="border: 1px solid black; border-radius: 25px; height: 30px; text-align: center;" required>
        <label for="angulo" style="font-style: italic; opacity: 0.7; word-wrap: break-word;">Ângulo da Trajetória</label>
      </div>

      <div style="display: flex; flex-direction: column; text-align: center; margin-bottom: 10px; width: 120px;">
        <input type="number" id="massa" name="massa" style="border: 1px solid black; border-radius: 25px; height: 30px; text-align: center;" required>
        <label for="massa" style="font-style: italic; opacity: 0.7; word-wrap: break-word;">Massa do Foguete</label>
      </div>

      <button type="button" onclick="simular()" style="display: flex; align-items: center; justify-content: center; background-color: black; color: white; border: none; border-radius: 25px; padding: 10px 20px; cursor: pointer; height: 30px;">Simular</button>
    </div>
  </form>

</div>

<script>
  function simular() {
    var pressao = document.getElementById('pressao').value;
    var volume = document.getElementById('volume').value;
    var angulo = document.getElementById('angulo').value;
    var massa = document.getElementById('massa').value;

    console.log("Valores inseridos: Pressão=" + pressao + ", Volume=" + volume + ", Ângulo=" + angulo + ", Massa=" + massa);
  }
</script>